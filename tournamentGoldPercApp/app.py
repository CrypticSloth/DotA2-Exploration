'''
NOTE!!!!!!!!!!1

This should actually work. I updated the wrong Procfile! for the wrong app!
Update the correct procfile with the correct stuff and you should be good
'''


import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import base64
import os
import search_engine
import time
from rq import Queue                    # requires Redis server (see readme)
from worker import conn                 # worker.py handles the connection to Redis
import uuid
from findPlayerGoldPerc import *

# initialize app
app = dash.Dash(__name__, static_folder='static')       # config to enable
app.scripts.config.serve_locally = True                   # things like css to
app.css.config.serve_locally = True                       # be served locally from /static
server = app.server                                     # folder


# get static images (recommended method is to load images as base64 strings)
static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
wiley_logo = base64.b64encode(open(os.path.join(static_folder, 'wiley.png'), 'rb').read())
robot_logo = base64.b64encode(open(os.path.join(static_folder, 'robot.png'), 'rb').read())

# markdown docs for layout
divider_markdown = '''
***
'''
description_markdown = '''
This is our boilerplate Dash app.
 '''
query_help_markdown = '''
We often use processes that take a while that would otherwise cause server and browser timeouts.
This app uses a background worker, automatic refreshing and a spinner to prevent timeouts and
provide an improved user experience.
'''

# initialize app layout
app.layout = html.Div(children=[

    # load stylesheets locally since they don't fetch from remote
    # locations when app is running on Heroku
    html.Link(href='/static/codepen.css', rel='stylesheet'),
    html.Link(href='/static/load_screen.css', rel='stylesheet'),

    # Our team's logo
    html.Div(
        html.Img(id='robot-logo',
            src='data:image/png;base64,{}'.format(robot_logo.decode()),
            style={'width': '100px'}), style={'display': 'inline', 'float': 'right', 'vertical-align': 'middle'}),

    # app name and description
    html.H1(children='Wiley Boilerplate Dash App'),
    dcc.Markdown(description_markdown),
    html.Br(),

    # query form and submit button
    # help text
    dcc.Markdown(query_help_markdown),
    html.Br(),

    # Submit
    html.Label('Press submit to start a 20 second process:'),
    html.Br(),
    dcc.Input(id='input-id', type='text', value="Match ID"),
    dcc.Input(id='input-time', type='text', value='Time'),
    html.Button(id='submit', type='submit', children='Submit'),
    html.Br(),
    html.Br(),

    # status infomation, e.g. "please wait"
    html.Div(id='status'),

    # invisible div to safely store the current job-id
    html.Div(id='job-id', style={'display': 'none'}),

    # this div is the target of the refresh during querying
    # initially there is no refresh (interval=1 hour) but during
    # a query it refreshes regularly until the results are ready
    html.Div([

        html.Div(children='', id='dummy-results'),
        dcc.Interval(
            id='update-interval',
            interval=60 * 60 * 5000,  # in milliseconds
            n_intervals=0
        )

    ], id='results'),

    # footer with corporate branding
    dcc.Markdown(children=divider_markdown),
    html.Div([
        html.Div(children='Put your legal notices, corporate logo or whatever here',
            style={'text-align': 'left', 'display': 'inline-block', 'vertical-align': 'middle'}),
    ], style={'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div(
        html.Img(id='wiley-logo',
            src='data:image/png;base64,{}'.format(wiley_logo.decode()),
            style={'width': '150px'}), style={'display': 'inline', 'float': 'right', 'vertical-align': 'middle'})

], style={'padding': '10px 10px'})


# this callback checks submits the query as a new job, returning job_id to the invisible div
@app.callback(
    dash.dependencies.Output('job-id', 'children'),
    [dash.dependencies.Input('submit', 'n_clicks')],
    [dash.dependencies.State('input-id', 'value'),
    dash.dependencies.State('input-time', 'value')])
def query_submitted(click, value_id, value_time):
    if click == 0 or click is None:
        return ''
    else:
        # a query was submitted, so queue it up and return job_id
        # data = collect_match_data(value_id)
        q = Queue(connection=conn)
        job_id = str(uuid.uuid4())
        job = q.enqueue_call(func=collect_match_data,
                                args=(value_id),
                                timeout='3m',
                                job_id=job_id)
        return job_id


# this callback checks if the job result is ready.  If it's ready
# the results return to the table.  If it's not ready, it pauses
# for a short moment, then empty results are returned.  If there is
# no job, then empty results are returned.
@app.callback(
    dash.dependencies.Output('dummy-results', 'children'),
    [dash.dependencies.Input('update-interval', 'n_intervals')],
    [dash.dependencies.State('job-id', 'children')])
def update_results_tables(n_intervals, job_id):
    q = Queue(connection=conn)
    job = q.fetch_job(job_id)
    if job is not None:
        # job exists - try to get result
        result = job.result
        if result is None:
            # results aren't ready, pause then return empty results
            # You will need to fine tune this interval depending on
            # your environment
            time.sleep(3)
            return ''
        if result is not None:
            # results are ready
            return result
    else:
        # no job exists with this id
        return ''


# this callback orders the table to be regularly refreshed if
# the user is waiting for results, or to be static (refreshed once
# per hour) if they are not.
@app.callback(
    dash.dependencies.Output('update-interval', 'interval'),
    [dash.dependencies.Input('job-id', 'children'),
    dash.dependencies.Input('update-interval', 'n_intervals')])
def stop_or_start_table_update(job_id, n_intervals):
    q = Queue(connection=conn)
    job = q.fetch_job(job_id)
    if job is not None:
        # the job exists - try to get results
        result = job.result
        if result is None:
            # a job is in progress but we're waiting for results
            # therefore regular refreshing is required.  You will
            # need to fine tune this interval depending on your
            # environment.
            return 1000
        else:
            # the results are ready, therefore stop regular refreshing
            return 60 * 60 * 1000
    else:
        # the job does not exist, therefore stop regular refreshing
        return 60 * 60 * 1000


# this callback displays a please wait message in the status div if
# the user is waiting for results, or nothing if they are not.
@app.callback(
    dash.dependencies.Output('status', 'children'),
    [dash.dependencies.Input('job-id', 'children'),
    dash.dependencies.Input('update-interval', 'n_intervals')])
def stop_or_start_table_update(job_id, n_intervals):
    q = Queue(connection=conn)
    job = q.fetch_job(job_id)
    if job is not None:
        # the job exists - try to get results
        result = job.result
        if result is None:
            # a job is in progress and we're waiting for results
            return 'Running query.  This might take a moment - don\'t close your browser!'
        else:
            # the results are ready, therefore no message
            return ''
    else:
        # the job does not exist, therefore no message
        return ''


# start the app
if __name__ == '__main__':
    app.run_server(debug=True)
