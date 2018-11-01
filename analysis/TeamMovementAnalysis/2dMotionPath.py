# See what we can do with a 2d graph of motion data
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from operator import itemgetter
sys.path.append('C:/GitHub/DotA2-Exploration/analysis')
from collectTeamData import search_matches_for_team
data_path = 'C:/GitHub/DotA2-Exploration/versions_test/'

# Get data
target_team = "Evil Geniuses"
target_versions = ["7.18"]
matches = search_matches_for_team(target_team, target_versions, progress_bar = True, path=data_path)

# Filter out motion data
motion_data = []
names = []

for i in range(5):
    motion_data.append(matches['radiant'][0]['players'][i]['eventData']['playerUpdatePositionEvents'])
    names.append(matches['radiant'][0]['players'][i]['name'])

# matches['radiant'][0]['match_id']
# sum([x['timeDead'] for x in matches['radiant'][0]['players'][0]['eventData']['deathEvents']])
# matches['radiant'][0]['players'][0]['eventData']['deathEvents']
# matches['radiant'][0]['duration'] + 89
# matches['radiant'][0]['players'][0]['eventData']['playerUpdatePositionEvents']

# Need to pad the data for when the player is not moving, as it does not record the time when the player is not moving
# This also happens when they are dead, the team jumps say 30 seconds when the player dies
# to fix this, detect whenever the time skips, and then use the most recent motion update coordinates for each missing time

padded_player_pos = []
for player_i in range(5):
    playerPosition = matches['radiant'][0]['players'][player_i]['eventData']['playerUpdatePositionEvents']
    for i in range(len(playerPosition)):
        # if next index is not one more than the previous time, then make that time have the same x and y as the most recent one
        now = playerPosition[i]
        next = playerPosition[i+1]
        if (now['time'] != (next['time'] + 1)):
            for x in range(next['time'] - now['time'] - 1):
                playerPosition.append({'time':(now['time'] + add), 'x':now['x'], 'y':now['y']})
                add += 1
            add = 1
    newPlayerPos = sorted(playerPosition, key=itemgetter('time'))
    padded_player_pos.append(newPlayerPos)

len(padded_player_pos)
len(padded_player_pos[0])
len(padded_player_pos[1])
len(padded_player_pos[2])
len(padded_player_pos[3])
len(padded_player_pos[4])

padded_player_pos[0][-1]
padded_player_pos[1][-1]
padded_player_pos[2][-1]
padded_player_pos[3][-1]
padded_player_pos[4][-1]

# Build the data frame
len(motion_data[0])
len(motion_data[1])
len(motion_data[2])
len(motion_data[3])
len(motion_data[4])
names

df = pd.DataFrame()

time = []
for i in motion_data[2]:
    time.append(i['time'])

df['time'] = time
for i in range(len(names)):
    x = []
    y = []
    for moment in motion_data[i]:
        x.append(moment['x'])
        y.append(moment['y'])
    for pad in range(len(time) - len(x)):
        x.append(moment['x'])
        y.append(moment['y'])
    print(len(time))
    print(len(x))
    print(len(y))
    df['{}_x'.format(names[i])] = x # Each player does not have the same amount of data (find the player with the most data and pad the rest of the players with 0's)
    df['{}_y'.format(names[i])] = y
    df['{}_xy'.format(names[i])] = np.array(x) + np.array(y)

df

# Plot it ######################

import plotly as py
import plotly.graph_objs as go

len(df['{}_xy'.format(names[0])])
# Create traces
trace0 = go.Scatter(
    x = df['time'],
    y = df['{}_xy'.format(names[0])],
    mode = 'lines',
    name = '{}_xy'.format(names[0])
)
# trace1 = go.Scatter(
#     x = df['time'],
#     y = df['{}_xy'.format(names[1])],
#     mode = 'lines',
#     name = '{}_xy'.format(names[1])
# )
# trace2 = go.Scatter(
#     x = df['time'],
#     y = df['{}_xy'.format(names[2])],
#     mode = 'lines',
#     name = '{}_xy'.format(names[2])
# )
# trace3 = go.Scatter(
#     x = df['time'],
#     y = df['{}_xy'.format(names[3])],
#     mode = 'lines',
#     name = '{}_xy'.format(names[3])
# )
# trace4 = go.Scatter(
#     x = df['time'],
#     y = df['{}_xy'.format(names[4])],
#     mode = 'lines',
#     name = '{}_xy'.format(names[4])
# )
# data = [trace0, trace1, trace2, trace3, trace4]
data = [trace0]

py.offline.plot(data, filename='line-mode')
