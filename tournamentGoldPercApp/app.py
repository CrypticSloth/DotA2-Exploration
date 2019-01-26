import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
import os
import findPlayerGoldPerc
import time
from rq import Queue                    # requires Redis server
from worker import conn                 # worker.py handles the connection to Redis
import uuid

def generate_table(dataframe, max_rows=1):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )

# initialize app
app = dash.Dash(__name__)       # config to enable
app.scripts.config.serve_locally=True                   # things like css to
app.css.config.serve_locally=True                       # be served locally from /assets
server = app.server                                     # folder

# get static images (recommended method is to load images as base64 strings)
static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets')
# wiley_logo = base64.b64encode(open(os.path.join(static_folder, 'wiley.png'), 'rb').read())
# robot_logo = base64.b64encode(open(os.path.join(static_folder, 'robot.png'), 'rb').read())

# markdown docs for layout
divider_markdown='''
***
'''

query_help_markdown='''
We often use processes that take a while that would otherwise cause server and browser timeouts.
This app uses a background worker, automatic refreshing and a spinner to prevent timeouts and
provide an improved user experience.
'''

# initialize app layout
app.layout = html.Div(children=[

    # load stylesheets locally since they don't fetch from remote
    # locations when app is running on Heroku
    html.Link(href='/assets/bootstrap.min.css',rel='stylesheet'),
    html.Link(href='/assets/codepen.css', rel='stylesheet'),
    html.Link(href='/assets/load_screen.css', rel='stylesheet'),
    html.Link(href='/assets/my_styles.css',rel='stylesheet'),

    html.H1('Dota Apps'),

    # Small Applet
    html.Div([
        html.H2('Players Net Worth Percentage (Small)'),
        html.H3('Instructions:'),
        html.Div('Put the match ID you are interested getting stats from in the first slot and put the time into the second slot.'),
        html.Div('Make sure the time is in the format like how you see it in game (MM:SS). For example: 10:35.'),
        html.Div('When you are ready, click RUN! '),
        dcc.Input(id='input-id', type='text', placeholder="Match ID",value= ""),
        dcc.Input(id='input-time', type='text', placeholder='Time',value=''),
        html.Button('Run', id='button'),
        dcc.Graph(
            id='perc-networth-plot'
            # figure={
            #     'data': create_plots(collect_match_data(4223661333),'10:0')
            # }
        ),
        html.Div([html.Table(id='my-table')], style={'width': '25%','display': 'inline-block', 'padding': '0 20'})
    ]),

    # Large Applet
    html.Div([
        html.H2('Player Network Percentage (Large)'),
        html.H3('Instructions:'),
        html.P(children=[
            'Put the match ID you are interested getting stats from in the first slot and put the time into the second slot.',
            html.Br(),
            'Make sure the time is in the format like how you see it in game (MM:SS). For example: 10:35.',
            html.Br(),
            'When you are ready, click RUN!'
        ]),

        dcc.Input(id='input-id-large', type='text', placeholder="Match ID", value=""),
        # dcc.Input(id='input-time', type='text', placeholder='Time',value=''),
        html.Button('Run', id='button_start', type='submit'),

        # status infomation, e.g. "please wait"
        html.Div(id='status'),

        # invisible div to safely store the current job-id
        html.Div(id='job-id', style={'display': 'none'}),

        # this div is the target of the refresh during querying
        # initially there is no refresh (interval=1 hour) but during
        # a query it refreshes regularly until the results are ready
        html.Div([

            dcc.Graph(id='dummy-results'),
            dcc.Interval(
                id='update-interval',
                interval=60*60*5000,  # in milliseconds
                n_intervals=0
            )

        ], id='results', style={'width':'75%','margin':25,'textAlign':'center'}),
    ]),

    # footer
    dcc.Markdown(children=divider_markdown),
        # ABOUT ROW
        html.Div(
            className='row',
            children=[
              html.Div(
                className='col',
                children=[
                  html.P(
                    'Data extracted from:'
                  ),
                  html.A(
                      'Stratz API',
                      href='https://stratz.com/'
                  )
                ]
              ),
              html.Div(
                className='col',
                children=[
                  html.P(
                    'Code avaliable at:'
                  ),
                  html.A(
                      'Github',
                      href='https://github.com/SorensenErik/DotA2-Exploration/tree/master/tournamentGoldPercApp'
                  )
                ]
              ),
              html.Div(
                className='col',
                children=[
                  html.P(
                    'Made with:'
                  ),
                  html.A(
                      'Dash / Plot.ly',
                      href='https://plot.ly/dash/'
                  )
                ]
              ),
              html.Div(
                className='col',
                children=[
                  html.P(
                    'Developer:'
                  ),
                  html.A(
                      'Erik Sorensen',
                      href='https://www.linkedin.com/in/erik-sorensen/'
                  )
                ]
              )
            ]
        ),
    ],
    style={
        'padding': 40
    }
)

# Callback for updating the output graph
@app.callback(
     Output(component_id='perc-networth-plot',component_property='figure'),
     [Input('button','n_clicks')],
     [State('input-id', 'value'),
     State('input-time', 'value')])
def update_value(n_clicks,value_id,value_time):
    print("running")
    if n_clicks > 0:
        df = findPlayerGoldPerc.faster_collect_match_data(value_id,value_time)

        return findPlayerGoldPerc.create_plots_fast(df)

# Callbacks for the small applet's table
@app.callback(
         Output(component_id='my-table',component_property='children'),
     [Input('button','n_clicks')],
     [State('input-id', 'value'),
     State('input-time', 'value')])
def update_value(n_clicks,value_id,value_time):
    print("running table")
    if n_clicks > 0:
        df = findPlayerGoldPerc.faster_collect_match_data(value_id,value_time)
        return generate_table(df)

# this callback checks submits the query as a new job, returning job_id to the invisible div
@app.callback(
    Output('job-id', 'children'),
     # Output(component_id='perc-networth-plot',component_property='figure'),
     [Input('button_start', 'n_clicks')],
     [State('input-id-large', 'value')])
def query_submitted(n_clicks, value_id):
    if n_clicks == 0 or n_clicks is None:
        return ''
    else:
        # a query was submitted, so queue it up and return job_id
        q = Queue(connection=conn)
        job_id = str(uuid.uuid4())
        job = q.enqueue_call(func=findPlayerGoldPerc.plot_perc_networth_overtime,
                                args=([value_id,5]), # Make sure the args are in a list
                                timeout='3m',
                                job_id=job_id)
        return job_id


# this callback checks if the job result is ready.  If it's ready
# the results return to the table.  If it's not ready, it pauses
# for a short moment, then empty results are returned.  If there is
# no job, then empty results are returned.
@app.callback(
    Output('dummy-results', 'figure'),
    [Input('update-interval', 'n_intervals')],
    [State('job-id', 'children')])
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
    Output('update-interval', 'interval'),
    [Input('job-id', 'children'),
    Input('update-interval', 'n_intervals')])
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
            return 60*60*1000
    else:
        # the job does not exist, therefore stop regular refreshing
        return 60*60*1000


# this callback displays a please wait message in the status div if
# the user is waiting for results, or nothing if they are not.
@app.callback(
    Output('status', 'children'),
    [Input('job-id', 'children'),
    Input('update-interval', 'n_intervals')])
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
