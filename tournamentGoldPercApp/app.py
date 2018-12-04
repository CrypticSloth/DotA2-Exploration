import os
os.chdir('C:/GitHub/DotA2-Exploration/tournamentGoldPercApp')
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
from findPlayerGoldPerc import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

ID = 4223661333
plot = create_plots(collect_match_data(ID),'10:0')

plot

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Players Net Worth Percentage'),
    dcc.Graph(
        id='perc_networth_plot',
        figure={
            'data': plot
        }
    )
    # dcc.Dropdown(
    #     id='dropdown',
    #     options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
    #     value='LA'
    # ),
    # html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
