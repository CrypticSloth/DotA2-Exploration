# Plot the ward map using plotly
# Eventually make a interactive webpage with dash 

from plotly import __version__
from plotly.offline import init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import numpy as np
import json

with open('../../versions_test/7.17/3944571593.json', 'r') as json_file:  
    data = json.load(json_file)

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
for i in range(len(data['players'])):
    print(data['players'][i]['personaname'])

# Get the players observer ward log for both teams

# Make the dictionaries we will place the data into
obs_wards_radiant = {
    '1_x':[],
    '1_y':[],
    '2_x':[],
    '2_y':[],
    '3_x':[],
    '3_y':[],
    '4_x':[],
    '4_y':[],
    '5_x':[],
    '5_y':[]
}

obs_wards_dire = {
    '1_x':[],
    '1_y':[],
    '2_x':[],
    '2_y':[],
    '3_x':[],
    '3_y':[],
    '4_x':[],
    '4_y':[],
    '5_x':[],
    '5_y':[]
}

sen_wards_radiant = {
    '1_x':[],
    '1_y':[],
    '2_x':[],
    '2_y':[],
    '3_x':[],
    '3_y':[],
    '4_x':[],
    '4_y':[],
    '5_x':[],
    '5_y':[]
}

sen_wards_dire = {
    '1_x':[],
    '1_y':[],
    '2_x':[],
    '2_y':[],
    '3_x':[],
    '3_y':[],
    '4_x':[],
    '4_y':[],
    '5_x':[],
    '5_y':[]
}

# Get ward data for radiant
for player in range(5):
    for i in range(len(data['players'][player]['obs_left_log'])):
        obs_wards_radiant['{:}_x'.format(player+1)].append(data['players'][player]['obs_left_log'][i]['x'])
        obs_wards_radiant['{:}_y'.format(player+1)].append(data['players'][player]['obs_left_log'][i]['y'])
    for i in range(len(data['players'][player]['sen_left_log'])):
        sen_wards_radiant['{:}_x'.format(player+1)].append(data['players'][player]['sen_left_log'][i]['x'])
        sen_wards_radiant['{:}_y'.format(player+1)].append(data['players'][player]['sen_left_log'][i]['y'])

# Get data for dire
for player in range(5,10):
    for i in range(len(data['players'][player]['obs_left_log'])):
        obs_wards_dire['{:}_x'.format(player-4)].append(data['players'][player]['obs_left_log'][i]['x'])
        obs_wards_dire['{:}_y'.format(player-4)].append(data['players'][player]['obs_left_log'][i]['y'])
    for i in range(len(data['players'][player]['sen_left_log'])):
        sen_wards_dire['{:}_x'.format(player-4)].append(data['players'][player]['sen_left_log'][i]['x'])
        sen_wards_dire['{:}_y'.format(player-4)].append(data['players'][player]['sen_left_log'][i]['y'])

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

Observer_Wards= go.Scatter(
                    x=x_obs,
                    y=y_obs,
                    mode='markers', 
                    marker = dict(color = "rgb(98, 244, 66)"))

Sentry_Wards= go.Scatter(
                    x=x_sent,
                    y=y_sent,
                    mode='markers', 
                    marker = dict(color = "rgb(65, 137, 244)"))
size = 128
layout= go.Layout(width=750,
                  height=750,
                  xaxis=dict(
                      autorange=False,
                      showgrid=False,
                      zeroline=False,
                      ticks='',
                      showticklabels=False,
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
fig=go.Figure(data=[Observer_Wards,Sentry_Wards],layout=layout)
plot(fig)