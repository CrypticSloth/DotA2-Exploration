# For reference
# https://dash.plot.ly/dash-core-components/input

import os
# os.chdir('C:/GitHub/DotA2-Exploration/tournamentGoldPercApp')
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from findPlayerGoldPerc import *

# NOTE!
# App times out, print statements do not fix it
# Must do something that the app uses

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_table(dataframe, max_rows=1):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )

# ID = 4247904407
# plot = create_plots(collect_match_data(ID),'10:0')
#
# plot

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Players Net Worth Percentage'),
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
])

# @app.callback(
#     Output(component_id='perc-networth-plot',component_property='figure'),
#     [Input(component_id='input-id',component_property='value'),
#      Input(component_id='input-time',component_property='value')])
# @app.callback(
#     Output(component_id='perc-networth-plot',component_property='figure'),
#     [Input('input-id', 'n_submit'), Input('input-id', 'n_blur'),
#     Input('input-time', 'n_submit'), Input('input-time', 'n_blur')],
#     [State('input-id', 'value'),
#     State('input-time', 'value')])
@app.callback(
     Output(component_id='perc-networth-plot',component_property='figure'),
     [Input('button','n_clicks')],
     [State('input-id', 'value'),
     State('input-time', 'value')])
def update_value(n_clicks,value_id,value_time):
    print("running")
    if n_clicks > 0:
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

    # print(ns1)
    # print(nb1)
    # print(ns2)
    # print(nb2)
    # print('______')

# def display_value(value):
#     return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
