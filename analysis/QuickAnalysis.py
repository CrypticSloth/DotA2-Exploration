import dota2api
import json
import numpy as np
#api = dota2api.Initialise("93B419AC20F968BA2CB66CA35B6CB654")

#api.get_live_league_games()

# How to request info from a page in python

import requests
page = requests.get('https://api.opendota.com/api/proMatches')
games = page.content

my_json = json.loads(games)
print(json.dumps(my_json,indent=4))

# Writing JSON data
with open('data.json', 'w') as f:
     json.dump(my_json, f)

# Reading data back
with open('data.json', 'r') as f:
     data = json.load(f)

print(type(data[1]['radiant_win']))

# My First dota analysis
# Based on this data which is 100 pro matches in the 7.07d patch
# Finding the average time of matches

time = []

for i in range(len(data)):
	time.append(data[i]['duration'])

# Convert list to numpy array for vector functionality
time = np.array(time)

# Convert from seconds to minutes
time = time / 60 

# Average Time of a game:
mean = np.mean(time)
print("Average length of pro games: {:.2f}".format(mean))

# Dire/Radiant win rate
winrate = []

for i in range(len(data)):
	winrate.append(data[i]['radiant_win'])

#winrate = np.array(winrate)
winrate = [1 if x == True else 0 for x in winrate]

print("Radiant winrate: {:.2f}".format(np.mean(winrate)))
