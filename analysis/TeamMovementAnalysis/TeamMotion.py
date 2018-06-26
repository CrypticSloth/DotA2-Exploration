import pandas as pd
import numpy as np
import json
import os
import requests
import matplotlib.pyplot as plt

# Reading data back
path = "C:/Users/Erik/Google Drive (erik.sorensen20@houghton.edu)/DotaAnalysis/versions_test/7.10/3781456589.json"

with open(path,'r') as outfile:
        data = json.load(outfile)

# The data we want is in players['eventData']['playerUpdatePositionEvents]
player_movement = data['players'][0]['eventData']['playerUpdatePositionEvents']

x = []
y = []
time = []
for i in range(len(player_movement)):
    x.append(int(player_movement[i]['x']))
    y.append(int(player_movement[i]['y']))
    time.append(int(player_movement[i]['time']))
    
print(min(x),max(x))
print(min(y),max(y))
print(max(time)/60)

plt.plot(x,y)
plt.title("'{}' movement".format(data['players'][0]['name']))
plt.show()

data['players'][0]['name']

# Reading data back
path = "C:/Users/Erik/Google Drive (erik.sorensen20@houghton.edu)/DotaAnalysis/versions_test/7.10/"

picks_bans = []
radiant_wins = []
for filename in os.listdir(path):
    with open(path + filename,'r') as outfile:
        data = json.load(outfile)
        picks_bans.append(data['picks_bans'])
        radiant_wins.append(data['radiant_win'])