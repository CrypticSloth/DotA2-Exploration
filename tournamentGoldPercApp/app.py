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

# ID = 4247904407
# plot = create_plots(collect_match_data(ID),'10:0')
#
# plot

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Players Net Worth Percentage'),
    dcc.Input(id='input-id', type='text', value= "Match ID"),
    dcc.Input(id='input-time', type='text', value='Time'),
    html.Button('Run', id='button'),
    dcc.Graph(
        id='perc-networth-plot'
        # figure={
        #     'data': create_plots(collect_match_data(4223661333),'10:0')
        # }
    )
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
    return create_plots(collect_match_data(value_id),value_time)
    # print(ns1)
    # print(nb1)
    # print(ns2)
    # print(nb2)
    # print('______')

# def display_value(value):
#     return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
