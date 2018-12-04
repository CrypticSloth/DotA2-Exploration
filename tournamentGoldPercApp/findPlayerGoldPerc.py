# make searchable by match id (from tourneys) the player gold perc of the teams perc at every time stamp
# Need to get the data in a dataframe where the gold for each player is there along with the time stamp and gold perc at that time stamp

# Note from Omegaman on what he wants
'''
1. percent of team's networth at any point in the game. Datdota has the raw values for each players networth at minute intervals. I want as percent of the team. I can do this manually in excel, but it takes me maybe half an hour per tournament to put it together
2. Basically all stats from datdota's "frames" available in a winning or losing format. In other words I want to be able to look at what a team or players networth/kills etc are in a win vs a loss
The questions i want to be able to ask are like "On NIP who is the player who if they have a bad first 10 minutes is most likely to lead to their team struggling?" so if Ace averages 4k networth at 10 minutes in wins and 3.8k networth in losses, but Fata averages 4k networth in wins and 3k in losses it appears like Fata is the key to their early game
That one sounds a lot hard
'''

import requests
import numpy as np
import pandas as pd
import json
from tqdm import tqdm

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
# offline.init_notebook_mode()
# plotly.offline.init_notebook_mode(connected=True)

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


    # ID = 4223661333
    page = requests.get('https://api.stratz.com/api/v1/match/{:}'.format(ID))
    games = page.content

    match = json.loads(games)

    df = pd.DataFrame()
    names = []
    for p in range(10):
        names.append(match['players'][p]['proPlayerName'])
        # names.append(match['players'][p]['name'])
    # match['players'][0]['eventData']['playerUpdateGoldEvents']
    time = []
    for i in range(len(match['players'][0]['eventData']['playerUpdateGoldEvents'])):
        if match['players'][0]['eventData']['playerUpdateGoldEvents'][i]['time'] > 0:
            time.append(match['players'][0]['eventData']['playerUpdateGoldEvents'][i]['time'])
    # Convert time format
    new_time = ['{:}:{:}'.format(divmod(sec,60)[0],divmod(sec,60)[1]) for sec in time]
    df['time'] = new_time
    len(time)

    for p in range(10):
        gold = []
        net_worth = []
        for x in range(len(match['players'][p]['eventData']['playerUpdateGoldEvents'])):
            if match['players'][p]['eventData']['playerUpdateGoldEvents'][x]['time'] > 0:
                gold.append(match['players'][p]['eventData']['playerUpdateGoldEvents'][x]['gold'])
                net_worth.append(match['players'][p]['eventData']['playerUpdateGoldEvents'][x]['networth'])
        df['{}_gold'.format(match['players'][p]['proPlayerName'])] = gold
        df['{}_networth'.format(match['players'][p]['proPlayerName'])] = net_worth

    # Add player percentage of net worth to the data frame
    # For inserting columns: DataFrame.insert(loc, column, value, allow_duplicates=False)
    # For iterating rows: for index, row in df.iterrows():
    #                          print row['c1'], row['c2']
    # Filter column names by df.filter(like="_networth")

    # This is reallllly slow: this needs to be sped up quite a bit!
    completed = 0
    for p in range(len(names)):
        networth_percentage = []
        for index, row in df.iterrows():
            rad_team = row[1:11]
            dire_team = row[11:]

            rad_team_networth = np.sum(rad_team.filter(like="_networth"))
            dire_team_networth = np.sum(dire_team.filter(like="_networth"))

            if p < 5:
                perc_networth = rad_team.filter(like="{}_networth".format(names[p])) / rad_team_networth
                networth_percentage.append(perc_networth[0])
            else:
                perc_networth = dire_team.filter(like="{}_networth".format(names[p])) / dire_team_networth
                networth_percentage.append(perc_networth[0])

        df['{}_networth_percentage'.format(names[p])] = networth_percentage
        completed += 10
        print("{}% completed".format(completed))
    return df

# test = collect_match_data()
# test
# seconds = 450
# divmod(seconds, 60)[1]
# test

def create_plots(dataframe, time):
    '''
    Create a plotly plot of the player gold percentage of both radiant and dire sides
    '''
    # dataframe = test
    # time = '10:0'

    df_time = dataframe['time']
    data = dataframe.filter(like="_networth_percentage")
    data['time'] = df_time

    time_index = 0
    for i in range(len(data['time'])):
        if str(data['time'][i]) == time:
            time_index = i

    data.iloc[0][0]

    int(data.iloc[time_index][0] * 100)

    data.columns[0].replace('_networth_percentage','')

    # Radiant
    rad1 = go.Bar(
        x=['radiant'],
        y=[data.iloc[time_index][0]],
        name=data.columns[0].replace('_networth_percentage','')
    )
    rad2 = go.Bar(
        x=['radiant'],
        y=[data.iloc[time_index][1]],
        name=data.columns[1].replace('_networth_percentage','')
    )
    rad3 = go.Bar(
        x=['radiant'],
        y=[data.iloc[time_index][2]],
        name=data.columns[2].replace('_networth_percentage','')
    )
    rad4 = go.Bar(
        x=['radiant'],
        y=[data.iloc[time_index][3]],
        name=data.columns[3].replace('_networth_percentage','')
    )
    rad5 = go.Bar(
        x=['radiant'],
        y=[data.iloc[time_index][4]],
        name=data.columns[4].replace('_networth_percentage','')
    )

    # Dire
    dire1 = go.Bar(
            x=['dire'],
            y=[data.iloc[time_index][5]],
            name=data.columns[5].replace('_networth_percentage','')
    )
    dire2 = go.Bar(
            x=['dire'],
            y=[data.iloc[time_index][6]],
            name=data.columns[6].replace('_networth_percentage','')
    )
    dire3 = go.Bar(
            x=['dire'],
            y=[data.iloc[time_index][7]],
            name=data.columns[7].replace('_networth_percentage','')
    )
    dire4 = go.Bar(
            x=['dire'],
            y=[data.iloc[time_index][8]],
            name=data.columns[8].replace('_networth_percentage','')
    )
    dire5 = go.Bar(
            x=['dire'],
            y=[data.iloc[time_index][9]],
            name=data.columns[9].replace('_networth_percentage','')
    )
    plot_data = [rad1,rad2,rad3,rad4,rad5,dire1,dire2,dire3,dire4,dire5]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=plot_data, layout=layout)
    # plotly.offline.plot(fig)
    return fig

if __name__ == '__main__':

    # Hour long Kuala Lumpuar EG vs NiP
    # Names are not correct for this match, needs fix
    create_plots(collect_match_data(4223661333),'10:0')
