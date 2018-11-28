# Here is how to collect data from stratz api
import requests
import json

# Get the most recent leagues (the ids are included)
# May be a bit late at registering as stratz is updated api league keys (11/26/18)
page = requests.get('https://api.stratz.com/api/v1/league')

# get the series data for a certain tournament ID
# 9870 is TI18
page = requests.get('https://api.stratz.com/api/v1/league/9870/series')

# Get all of the matches under that tournament id
page = requests.get('https://api.stratz.com/api/v1/league/{id}/matches')

def most_x_recent_tourney_id(x = 5):
    '''
    Collect the most recent tournament ID
    Could be delayed if stratz has not updated api keys yet
    '''

    page = requests.get('https://api.stratz.com/api/v1/league')
    games = page.content

    proMatches = json.loads(games)

    for i in range(x):
        id = proMatches[i]['id']
        name = proMatches[i]['name']
        print("name:" + str(name))
        print("ID:" + str(id))
        print("------------")

most_x_recent_tourney_id(10)

def list_tourney_match_ids(tourneyID):

    page = requests.get('https://api.stratz.com/api/v1/league/{}/series?take=250'.format(tourneyID))
    games = page.content

    matches = json.loads(games)
    match_ids = []
    matches['results'][0]['matches']
    for series in matches['results']:
        for match in series['matches']:
            match_ids.append(match['id'])

    # matches['results'][3]['matches']
    # match_ids = []
    # for match in matches['results']:
    #     match_ids.append(match['id'])
    return match_ids

TI8_match_ids = list_tourney_match_ids(9870)
TI8_match_ids
