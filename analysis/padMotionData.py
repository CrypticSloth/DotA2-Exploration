# Functions to extract and clean motion data from games extracted with collectTeamData.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from operator import itemgetter
from collections import defaultdict
from analysis.collectTeamData import search_matches_for_team

def padMotionData(data, faction = "", match_id):
    '''
    Function to sift through team movement data (from the function search_matches_for_team in collectTeamData.py).
    Returns a pandas dataframe with cleaned and padded movement data
    Padded means that motion is added to each players data because the api does not count the coordinates for each second
        where the player is not moving (only updates new movement coordinates) the padding fills in that missing data.
        The data is also padded at the last second as there were some discrepancies between each player at the end, each
        player did not end at the same time (probably due to each player logging out at different times)

    Inputs:
        data (required) - the data should be the return of the function search_matches_for_team
        faction (optional) - either 'radiant' or 'dire'
        game_id (optional) - if there is a specific match_id you are looking for inside the data collected you can put it here

    Outputs:
        A dictionary of dataframes of movement data, split into radiant and dire.
    '''

    data = search_matches_for_team("Evil Geniuses",["7.18"],progress_bar=True, path="C:/GitHub/DotA2-Exploration/versions_test")
    faction = "radiant"
    motion_data = []
    names = []

    cleanedData = defaultdict(list)

    radiant = padFactionData(data,'radiant')
    dire = padFactionData(data,'dire')

    cleanedData['radiant'].append(radiant)
    cleanedData['dire'].append(dire)


# Use code below, code above is the wrong way to go about it i think

def padFactionData(data,faction):
    dfs = []
    # Loop through each match on both radiant and dire
    for match_i in range(len(data[faction])):
        motion_data = []
        names = []
        for i in range(10):
            motion_data.append(data[faction][match_i]['players'][i]['eventData']['playerUpdatePositionEvents'])
            names.append(data[faction][match_i]['players'][i]['name'])

        padded_player_pos = []
        for player_i in range(10):
            playerPosition = data[faction][match_i]['players'][player_i]['eventData']['playerUpdatePositionEvents']
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

        lens = [len(motion_data[0]),len(motion_data[1]),len(motion_data[2]),len(motion_data[3]),len(motion_data[4])]
        names

        def findMaxIndex(lens):
            max = -1
            max_index = 0
            for i in range(len(lens)):
                if lens[i] > max:
                    max = lens[i]
                    max_index = i
            return max_index

        longestMatchIndex = findMaxIndex(lens)
        time = []
        # !!!!! Need to choose the index with the most time
        for i in motion_data[longestMatchIndex]:
            time.append(i['time'])

        df = pd.DataFrame()

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
            # print(len(time))
            # print(len(x))
            # print(len(y))
            df['{}_x'.format(names[i])] = x # Each player does not have the same amount of data (find the player with the most data and pad the rest of the players with 0's)
            df['{}_y'.format(names[i])] = y
            df['{}_xy'.format(names[i])] = np.array(x) + np.array(y)

        dfs.append(df)

    return dfs


def putTogether(data):
    cleanedData = defaultdict(list)

    radiant = padFactionData(data,'radiant')
    dire = padFactionData(data,'dire')

    cleanedData['radiant'].append(radiant)
    cleanedData['dire'].append(dire)

    return cleanedData

if __name__ == '__main__':

    target_team = "Evil Geniuses"
    target_versions = ["7.18"]
    data = search_matches_for_team(target_team,target_versions,progress_bar=True, path="C:/GitHub/DotA2-Exploration/versions_test")

    matches = putTogether(data)

    matches['dire']
