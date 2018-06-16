
# coding: utf-8

# In[33]:


# Dota Analysis of wards placed to winrate
# Make a scatter plot where win or loss will be coded as a green or red dot
# This is to easily see a trend of wards placed to win rate
# Data is of lower mmr placed where there will be a greater variance of wards placed
# Also the data will need to be set between a certain amount of time so that extra long games where more wards could be placed dont skew the graph
# My hypothesis is that games where more wards are placed will have a higher average winrate

import requests
import matplotlib.pyplot
import json 
import numpy as np


# In[47]:


#Get most recent match so we can grab different data every time in the next block
page = requests.get("https://api.opendota.com/api/publicMatches")
games = page.content
games = json.loads(games)
recent_game = games[0]['match_id']
recent_game


# In[ ]:


# Pull pub match data
data = []
for i in range(250):
    page = requests.get("https://api.opendota.com/api/publicMatches?less_than_match_id={:}".format(recent_game - (i*10000)))
    games = page.content
    games = json.loads(games)
    data.append(games)


# In[103]:


#flatten the data
flat_data = []
for call in data:
    for match in call:
        flat_data.append(match)


# In[104]:


flat_data


# In[105]:


# Only grab the matches that have a avg_rank_tier between 0 and 30 and whos duration is between 1650 and 1799 (median time is 1676)
matches = []
for match in flat_data:
    if ((match['avg_rank_tier'] < 30) & ((match['duration'] > 1650) & (match['duration'] < 1799))):
        matches.append(match['match_id'])
        
len(set(matches))


# In[ ]:




