import os
# os.chdir('C:/GitHub/DotA2-Exploration/tournamentGoldPercApp') # for atom hydrogen
import plotly
import dash
import dash_bootstrap_components as dbc # For loading bars
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from findPlayerGoldPerc import *

def generate_table(dataframe, max_rows=1):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
        'rel':'stylesheet',
        'integrity': 'sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# Initialize the pages base html code with custom html
with open('baseHTML.html', 'r') as file:
    app.index_string = file.read()

app.layout = html.Div([

    html.Div([
        html.H4('Warning:'),
        html.P("Some match id's will not work if they have not been parsed by the Stratz API. All professional games should be parsed, but if not, the graphs will not load.")
    ]),

    html.Div([
        html.H2('Player Network Percentage Over Time'),
        html.H3('Instructions:'),
        html.P(children=[
            'This app returns a plot of each players percentage of thier teams total networth over time.',
            html.Br(),
            'Simply enter in the id of the game you would like to analyze and click RUN!'
        ]),
        html.Div(className='container',children=[
            html.Div(className='row justify-content-start', children=[
                html.Div(className='col align-self-start',children=[
                    dcc.Input(className='form-control',id='input-id-large', type='text', placeholder="Match ID", value="4223661333"),
                ]),
                html.Div(className='col align-self-start',children=[
                    html.Button('Run', className='btn btn-primary', id='button_large', type='submit'),
                ]),
                html.Div(className='col align-self-start',children=[
                    dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")], type="default", fullscreen=False),
                ])
            ])
        ]),

        # status infomation, e.g. "please wait"
        html.Div(id='status'),

        # invisible div to safely store the current job-id
        html.Div(id='job-id', style={'display': 'none'}),

        # this div is the target of the refresh during querying
        # initially there is no refresh (interval=1 hour) but during
        # a query it refreshes regularly until the results are ready
        html.Div([

            dcc.Graph(id='large-results'),
            dcc.Interval(
                id='update-interval',
                interval=60*60*5000,  # in milliseconds
                n_intervals=0
            )

        ], id='results', style={'width':'75%','margin':25,'textAlign':'center'}),
    ]),

    html.Div([
        html.H2('Players Net Worth Percentage at One Time'),
        html.H3('Instructions:'),
        html.Div('Put the match ID you are interested getting stats from in the first slot and put the time into the second slot.'),
        html.Div('Make sure the time is in the format like how you see it in game (MM:SS). For example: 10:30.'),
        html.Div('When you are ready, click RUN! '),
        dcc.Input(id='input-id', type='text', placeholder="Match ID",value= "4223661333"),
        dcc.Input(id='input-time', type='text', placeholder='Time',value='10:30'),
        html.Button('Run', id='button'),
        html.Div([
            dcc.Graph(
                id='perc-networth-plot'
            ),
        ], style={'width':'75%','margin':25,'textAlign':'center'}),
        html.Div([html.Table(id='my-table')], style={'width': '25%','display': 'inline-block', 'padding': '0 20'})
    ]),
])

@app.callback(
     Output(component_id='perc-networth-plot',component_property='figure'),
     [Input('button','n_clicks')],
     [State('input-id', 'value'),
     State('input-time', 'value')])
def update_value(n_clicks,value_id,value_time):
    print("running")
    if n_clicks > 0: # This throws an error for some reason
        df = faster_collect_match_data(value_id,value_time)
        return create_plots_fast(df)

@app.callback(
     Output(component_id='my-table',component_property='children'),
     [Input('button','n_clicks')],
     [State('input-id', 'value'),
     State('input-time', 'value')])
def update_value(n_clicks,value_id,value_time):
    print("running table")
    if n_clicks > 0:
        df = faster_collect_match_data(value_id,value_time)
        return generate_table(df)

@app.callback(
    [Output(component_id='large-results',component_property='figure'),
    Output("loading-output-1", "children")],
    [Input('button_large','n_clicks')],
    [State('input-id-large','value')])
def plot_large(n_clicks,value_id):
    print("running large graph")
    if n_clicks > 0:
        return plot_perc_networth_overtime(value_id, 30),None # The none is there for the second output which controls the loading bar
        # return plot_perc_networth_overtime(value_id, 30), None # The none is there for the second output which controls the loading bar

if __name__ == '__main__':
    app.run_server(debug=True)
