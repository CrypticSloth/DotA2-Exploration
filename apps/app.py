import plotly
import numpy as np
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

##############################
### Get all the data ready ###
##############################

match = 3944571593
with open('{:}.json'.format(match), 'r') as json_file:  
    data = json.load(json_file)

import time
time.strftime('%M:%S', time.gmtime(1200))

# Get player names
player_names = []
for i in range(len(data['players'])):
    player_names.append(data['players'][i]['personaname'])

# Get the players observer ward log for both teams

# Make the dictionaries we will place the data into
obs_wards_radiant = {
    '1_x':[],
    '1_y':[],
    '1_time':[],
    '2_x':[],
    '2_y':[],
    '2_time':[],
    '3_x':[],
    '3_y':[],
    '3_time':[],
    '4_x':[],
    '4_y':[],
    '4_time':[],
    '5_x':[],
    '5_y':[],
    '5_time':[]
}

obs_wards_dire = {
    '1_x':[],
    '1_y':[],
    '1_time':[],
    '2_x':[],
    '2_y':[],
    '2_time':[],
    '3_x':[],
    '3_y':[],
    '3_time':[],
    '4_x':[],
    '4_y':[],
    '4_time':[],
    '5_x':[],
    '5_y':[],
    '5_time':[]
}

sen_wards_radiant = {
    '1_x':[],
    '1_y':[],
    '1_time':[],
    '2_x':[],
    '2_y':[],
    '2_time':[],
    '3_x':[],
    '3_y':[],
    '3_time':[],
    '4_x':[],
    '4_y':[],
    '4_time':[],
    '5_x':[],
    '5_y':[],
    '5_time':[]
}

sen_wards_dire = {
    '1_x':[],
    '1_y':[],
    '1_time':[],
    '2_x':[],
    '2_y':[],
    '2_time':[],
    '3_x':[],
    '3_y':[],
    '3_time':[],
    '4_x':[],
    '4_y':[],
    '4_time':[],
    '5_x':[],
    '5_y':[],
    '5_time':[]
}

# Get ward data for radiant
for player in range(5):
    for i in range(len(data['players'][player]['obs_left_log'])):
        obs_wards_radiant['{:}_x'.format(player+1)].append(data['players'][player]['obs_left_log'][i]['x'])
        obs_wards_radiant['{:}_y'.format(player+1)].append(data['players'][player]['obs_left_log'][i]['y'])
        obs_wards_radiant['{:}_time'.format(player+1)].append(time.strftime('%M:%S', time.gmtime(data['players'][player]['obs_left_log'][i]['time'])))
    for i in range(len(data['players'][player]['sen_left_log'])):
        sen_wards_radiant['{:}_x'.format(player+1)].append(data['players'][player]['sen_left_log'][i]['x'])
        sen_wards_radiant['{:}_y'.format(player+1)].append(data['players'][player]['sen_left_log'][i]['y'])
        sen_wards_radiant['{:}_time'.format(player+1)].append(time.strftime('%M:%S', time.gmtime(data['players'][player]['sen_left_log'][i]['time'])))

# Get data for dire
for player in range(5,10):
    for i in range(len(data['players'][player]['obs_left_log'])):
        obs_wards_dire['{:}_x'.format(player-4)].append(data['players'][player]['obs_left_log'][i]['x'])
        obs_wards_dire['{:}_y'.format(player-4)].append(data['players'][player]['obs_left_log'][i]['y'])
        obs_wards_dire['{:}_time'.format(player-4)].append(time.strftime('%M:%S', time.gmtime(data['players'][player]['obs_left_log'][i]['time'])))
    for i in range(len(data['players'][player]['sen_left_log'])):
        sen_wards_dire['{:}_x'.format(player-4)].append(data['players'][player]['sen_left_log'][i]['x'])
        sen_wards_dire['{:}_y'.format(player-4)].append(data['players'][player]['sen_left_log'][i]['y'])
        sen_wards_dire['{:}_time'.format(player-4)].append(time.strftime('%M:%S', time.gmtime(data['players'][player]['sen_left_log'][i]['time'])))

traces = []
for i in range(5):
    if obs_wards_radiant['{:}_x'.format(i+1)] != []:
        trace0=go.Scatter(
            x=obs_wards_radiant['{:}_x'.format(i+1)],
            y=obs_wards_radiant['{:}_y'.format(i+1)],
            name=player_names[i],
            text=obs_wards_radiant['{:}_time'.format(i+1)],
            mode='markers',
            marker = dict(color = "rgb(98, 244, 66)"),
            hoverlabel=dict(
                      bgcolor='black',
                      bordercolor='rgb(98, 244, 66)'
                  )
        )
    if obs_wards_dire['{:}_x'.format(i+1)] != []:
        trace1=go.Scatter(
            x=obs_wards_dire['{:}_x'.format(i+1)],
            y=obs_wards_dire['{:}_y'.format(i+1)],
            name=player_names[i+5],
            text=obs_wards_dire['{:}_time'.format(i+1)],
            mode='markers', 
            marker = dict(color = "rgb(98, 244, 66)"),
                        hoverlabel=dict(
                      bgcolor='black',
                      bordercolor='rgb(98, 244, 66)'
                  ),
        )
    if sen_wards_radiant['{:}_x'.format(i+1)] != []:
        trace2=go.Scatter(
            x=sen_wards_radiant['{:}_x'.format(i+1)],
            y=sen_wards_radiant['{:}_y'.format(i+1)],
            name=player_names[i],
            text=sen_wards_radiant['{:}_time'.format(i+1)],
            mode='markers',
            marker = dict(color = "rgb(26, 140, 255)"),
            hoverlabel=dict(
                      bgcolor='black',
                      bordercolor='rgb(26, 140, 255)'
                  ),
        )
    if sen_wards_dire['{:}_x'.format(i+1)] != []:
        trace3=go.Scatter(
            x=sen_wards_dire['{:}_x'.format(i+1)],
            y=sen_wards_dire['{:}_y'.format(i+1)],
            name=player_names[i+5],
            text=sen_wards_dire['{:}_time'.format(i+1)],
            mode='markers', 
            marker = dict(color = "rgb(26, 140, 255)"),
                        hoverlabel=dict(
                      bgcolor='black',
                      bordercolor='rgb(26, 140, 255)'
                  ),
        )
    traces.append(trace0)
    traces.append(trace1)
    traces.append(trace2)
    traces.append(trace3)

# Create shape objects
shapes_obs_x_rad = []
shapes_obs_y_rad = []
shapes_obs_x_dire = []
shapes_obs_y_dire = []

shapes_sen_x_rad = []
shapes_sen_y_rad = []
shapes_sen_x_dire = []
shapes_sen_y_dire = []

for i in range(5):
    shapes_obs_x_rad.append(obs_wards_radiant['{:}_x'.format(i+1)])
    shapes_obs_y_rad.append(obs_wards_radiant['{:}_y'.format(i+1)])
    shapes_obs_x_dire.append(obs_wards_dire['{:}_x'.format(i+1)])
    shapes_obs_y_dire.append(obs_wards_dire['{:}_y'.format(i+1)])
    shapes_sen_x_rad.append(sen_wards_radiant['{:}_x'.format(i+1)])
    shapes_sen_y_rad.append(sen_wards_radiant['{:}_y'.format(i+1)])
    shapes_sen_x_dire.append(sen_wards_dire['{:}_x'.format(i+1)])
    shapes_sen_y_dire.append(sen_wards_dire['{:}_y'.format(i+1)])

shapes_obs_x_rad = [item for sublist in shapes_obs_x_rad for item in sublist]
shapes_obs_y_rad = [item for sublist in shapes_obs_y_rad for item in sublist]
shapes_obs_x_dire = [item for sublist in shapes_obs_x_dire for item in sublist]
shapes_obs_y_dire = [item for sublist in shapes_obs_y_dire for item in sublist]
shapes_sen_x_rad = [item for sublist in shapes_sen_x_rad for item in sublist]
shapes_sen_y_rad = [item for sublist in shapes_sen_y_rad for item in sublist]
shapes_sen_x_dire = [item for sublist in shapes_sen_x_dire for item in sublist]
shapes_sen_y_dire = [item for sublist in shapes_sen_y_dire for item in sublist]

shapes = []
for i in range(len(shapes_obs_x_rad)):
    shape0=dict(
        type='circle',
        xref='x',
        yref='y',
        x0=shapes_obs_x_rad[i] - 10, # Obs wards have a radius of 10. so subtract 10 from x0 and y0 and add 10 to x1,y1
        y0=shapes_obs_y_rad[i] - 10, # Cant do a list of coordinates so will have to make multiple shape objects
        x1=shapes_obs_x_rad[i] + 10,
        y1=shapes_obs_y_rad[i] + 10,
        fillcolor='rgba(50, 171, 96, 0.1)',
        line=dict(  
            color='rgba(50, 171, 96, 1)'
        ),
    )
    shapes.append(shape0)

for i in range(len(shapes_obs_x_dire)):
    shape0=dict(
        type='circle',
        xref='x',
        yref='y',
        x0=shapes_obs_x_dire[i] - 10, 
        y0=shapes_obs_y_dire[i] - 10, 
        x1=shapes_obs_x_dire[i] + 10,
        y1=shapes_obs_y_dire[i] + 10,
        fillcolor='rgba(50, 171, 96, 0.1)',
        line=dict(  
            color='rgba(255, 0, 57,1)'
        ),
    )
    shapes.append(shape0)

for i in range(len(shapes_sen_x_rad)):
    shape0=dict(
        type='circle',
        xref='x',
        yref='y',
        x0=shapes_sen_x_rad[i] - 5.5, # sent wards have a radius of about 5.5
        y0=shapes_sen_y_rad[i] - 5.5, 
        x1=shapes_sen_x_rad[i] + 5.5,
        y1=shapes_sen_y_rad[i] + 5.5,
        fillcolor='rgba(0, 102, 255,0.1)',
        line=dict(  
            color='rgba(50, 171, 96, 1)'
        ),
    )
    shapes.append(shape0)

for i in range(len(shapes_sen_x_dire)):
    shape0=dict(
        type='circle',
        xref='x',
        yref='y',
        x0=shapes_sen_x_dire[i] - 5.5,
        y0=shapes_sen_y_dire[i] - 5.5,
        x1=shapes_sen_x_dire[i] + 5.5,
        y1=shapes_sen_y_dire[i] + 5.5,
        fillcolor='rgba(0, 102, 255,0.1)',
        line=dict(  
            color='rgba(255, 0, 57,1)'
        ),
    )
    shapes.append(shape0)

size = 128
layout= go.Layout(width=750,
                  height=750,
                  hovermode= 'closest',
                  title="Ward map of match: {:}".format(match),
                  showlegend=False,
                  xaxis=dict(
                      autorange=False,
                      showgrid=False,
                      zeroline=False,
                      ticks='',
                      showticklabels=False,
                      # coordinates are [63,192]
                      range=[63,192],
                  ),
                  yaxis=dict(
                      autorange=False,
                      showgrid=False,
                      zeroline=False,
                      ticks='',
                      showticklabels=False,
                      range=[63,192]
                  ),
                  images= [dict(
                  source= "https://raw.githubusercontent.com/SorensenErik/DotA2-Exploration/master/analysis/TeamWardAnalysis/detailed_707.jpg",
                  xref= "x",
                  yref= "y",
                  x= 63,
                  y= 192,
                  sizex= size,
                  sizey= size,
                  sizing= "stretch",
                  layer= "below",
                  )],
                  shapes=shapes)

fig = go.Figure(data=traces,layout=layout)
#plot(fig)

#########################
### Make the dash app ###
#########################

app = dash.Dash()
server=app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.css.append_css({'external_url':'/static/reset.css'})
app.server.static_folder = 'static'

colors = {
    'background': '#303059',
    'text': '#FFFFFF'
}

# Update plots colors with theme of dash app
fig['layout']['plot_bgcolor'] = colors['background']
fig['layout']['paper_bgcolor'] = colors['background']
fig['layout']['font'] = {'color':colors['text']}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    
    html.H1(children='Dota match: {:}'.format(match),
            style={'color':colors['text']}),
    html.Div(children="A ward map made with plotly and dash",
            style={'color':colors['text']}),

    dcc.Graph(id='dota-ward-graph',
              figure=fig)
    # dcc.Slider(
    #     id='year-slider',
    #     min=df['year'].min(),
    #     max=df['year'].max(),
    #     value=df['year'].min(),
    #     step=None,
    #     marks={str(year): str(year) for year in df['year'].unique()}
    # )
])


# @app.callback(
#     dash.dependencies.Output('graph-with-slider', 'figure'),
#     [dash.dependencies.Input('year-slider', 'value')])
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
#     traces = []
#     for i in filtered_df.continent.unique():
#         df_by_continent = filtered_df[filtered_df['continent'] == i]
#         traces.append(go.Scatter(
#             x=df_by_continent['gdpPercap'],
#             y=df_by_continent['lifeExp'],
#             text=df_by_continent['country'],
#             mode='markers',
#             opacity=0.7,
#             marker={
#                 'size': 15,
#                 'line': {'width': 0.5, 'color': 'white'}
#             },
#             name=i
#         ))

#     return {
#         'data': traces,
#         'layout': go.Layout(
#             xaxis={'type': 'log', 'title': 'GDP Per Capita'},
#             yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#             legend={'x': 0, 'y': 1},
#             hovermode='closest'
#         )
#     }


if __name__ == '__main__':
    app.run_server(debug=True,port=9000)