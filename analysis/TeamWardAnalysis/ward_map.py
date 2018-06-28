# Plot the ward map using plotly
# Eventually make a interactive webpage with dash 

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import json

with open('../../versions_test/7.17/3944571593.json', 'r') as json_file:  
    data = json.load(json_file)

# Get player name
data["players"][0]["personaname"]

# Get the players observer ward log
data['players'][0]['obs_log']
data['players'][0]['sen_log']

x_obs = []
y_obs = []
x_sent = []
y_sent = []



for i in data['eventData']['wardEvents']:
    if i['x'] != 0:
        if i['wardType'] == 0:
            x_obs.append(i['x'])
            y_obs.append(i['y'])
        else if i['wardType'] == 1:
            x_sent.append(i['x'])
            y_sent.append(i['y'])

trace1= go.Scatter(x=[0,0.5,1,2,2.2],y=[1.23,2.5,0.42,3,1])
layout= go.Layout(images= [dict(
                  source= "actualWards.png",
                  xref= "x",
                  yref= "y",
                  x= 0,
                  y= 3,
                  sizex= 2,
                  sizey= 2,
                  sizing= "stretch",
                  opacity= 0.5,
                  layer= "below")])

fig=go.Figure(data=[trace1],layout=layout)
plotly.offline.plot(fig)