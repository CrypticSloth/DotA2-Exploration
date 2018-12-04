# For reference
# https://dash.plot.ly/dash-core-components/input

import os
os.chdir('C:/GitHub/DotA2-Exploration/tournamentGoldPercApp')
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from findPlayerGoldPerc import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# ID = 4247904407
# plot = create_plots(collect_match_data(ID),'10:0')
#
# plot

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Players Net Worth Percentage'),
    dcc.Input(id='input-id', type='number', value= "Match ID",debounce=True),
    dcc.Input(id='input-time', type='text', value='Time',debounce=True),
    dcc.Graph(
        id='perc-networth-plot'
        # figure={
        #     'data': create_plots(collect_match_data(4223661333),'10:0')
        # }
    )
])

@app.callback(
    Output(component_id='perc-networth-plot',component_property='figure'),
    [Input(component_id='input-id',component_property='value'),
     Input(component_id='input-time',component_property='value')])
def update_value(value_id,value_time):
    return create_plots(collect_match_data(value_id),value_time)

# def display_value(value):
#     return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
