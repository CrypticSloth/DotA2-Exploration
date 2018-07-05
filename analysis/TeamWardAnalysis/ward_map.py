# Plot the ward map using plotly
# Eventually make a interactive webpage with dash 

from plotly import __version__
from plotly.offline import init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import numpy as np
import json

match = 3944571593
with open('../../versions_test/7.17/{:}.json'.format(match), 'r') as json_file:  
    data = json.load(json_file)

import time
time.strftime('%M:%S', time.gmtime(1200))

# Lets test another matches ward map to see if it holds out
# with open('../../versions_test/7.18/3973127831.json', 'r') as json_file:  
#     data_test = json.load(json_file)

# x_obs = []
# y_obs = []
# x_sent = []
# y_sent = []

# for i in data_test['eventData']['wardEvents']:
#     if i['x'] != 0:
#         if i['wardType'] == 0:
#             x_obs.append(i['x'])
#             y_obs.append(i['y'])
#         if i['wardType'] == 1:
#             x_sent.append(i['x'])
#             y_sent.append(i['y'])

# Hooray this does work with other files which means it works as expected

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

x_obs = []
y_obs = []
x_sent = []
y_sent = []

for i in data['eventData']['wardEvents']:
    if i['x'] != 0:
        if i['wardType'] == 0:
            x_obs.append(i['x'])
            y_obs.append(i['y'])
        if i['wardType'] == 1:
            x_sent.append(i['x'])
            y_sent.append(i['y'])

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
                  layer= "below")])

# Plot to html file
fig=go.Figure(data=traces,layout=layout)
plot(fig)