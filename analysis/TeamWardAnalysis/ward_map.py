# Plot the ward map using plotly
# Eventually make a interactive webpage with dash 

from plotly import __version__
from plotly.offline import init_notebook_mode, plot, iplot
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
        if i['wardType'] == 1:
            x_sent.append(i['x'])
            y_sent.append(i['y'])

trace1= go.Scatter(x=x_obs + x_sent,y=y_obs + y_sent,
                   mode='markers', 
                   marker = dict(color = "rgb(241, 244, 66)"))
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
                  source= "https://raw.githubusercontent.com/SorensenErik/DotA2-Exploration/master/analysis/TeamWardAnalysis/actualWards.png",
                  xref= "x",
                  yref= "y",
                  x= 63,
                  y= 192,
                  sizex= size,
                  sizey= size,
                  sizing= "stretch",
                  layer= "below")])

# Plot to html file
fig=go.Figure(data=[trace1],layout=layout)
plot(fig)