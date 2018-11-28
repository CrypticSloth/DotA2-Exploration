# make searchable by match id (from tourneys) the player gold perc of the teams perc at every time stamp
# Need to get the data in a dataframe where the gold for each player is there along with the time stamp and gold perc at that time stamp

import requests
import numpy as np
import pandas as pd
import json

def collect_league_data():
    '''
    Get league data from stratz api and strip it of all un-useful data. Want it in a data frame format.
    We need to collect each players net worth at every timestamp and put that into a dataframe

    Question is how to sort through this data?
        There are many teams and matches. How to sort them into neat, easily accessible data frames?

        Omegaman wants it by match. So maybe Match ID, or save it in a way where the team names are shown?
    '''

    return team_data

def collect_match_data(ID = 4238597779):
    '''
    Lets start easy and start with getting individual match data per match id

    Function will parse a match id for player gold on both sides with player gold percentages at each moment in the game.
    '''

    page = requests.get('https://api.stratz.com/api/v1/match/{:}'.format(ID))
    games = page.content

    match = json.loads(games)

    df = pd.DataFrame()
    match['players'][0]['name']
    # match['players'][0]['eventData']['playerUpdateGoldEvents']
    time = []
    for i in range(len(match['players'][0]['eventData']['playerUpdateGoldEvents'])):
        if match['players'][0]['eventData']['playerUpdateGoldEvents'][i]['time'] > 0:
            time.append(match['players'][0]['eventData']['playerUpdateGoldEvents'][i]['time'])
    df['time'] = time
    len(time)

    for p in range(10):
        gold = []
        net_worth = []
        for x in range(len(match['players'][p]['eventData']['playerUpdateGoldEvents'])):
            if match['players'][p]['eventData']['playerUpdateGoldEvents'][x]['time'] > 0:
                gold.append(match['players'][p]['eventData']['playerUpdateGoldEvents'][x]['gold'])
                net_worth.append(match['players'][p]['eventData']['playerUpdateGoldEvents'][x]['networth'])
        df['{}_gold'.format(match['players'][p]['name'])] = gold
        df['{}_networth'.format(match['players'][p]['name'])] = net_worth

    return df
