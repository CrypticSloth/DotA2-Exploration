# Loop through data files and collect only the match IDs that have a certain team in it
import json
import os, os.path
from collections import defaultdict

path = '../versions_test'
game_version = '7.18'
match = '3967478661'

with open('{:}/{:}/{:}.json'.format(path, game_version, match),'r') as outfile:
    data = json.load(outfile)

radiant_team  = data['pro_team_data'][2]['radiant_name']
dire_team  = data['pro_team_data'][4]['dire_name']
tournament_name = data['pro_team_data'][6]['league_name']


def search_matches_for_team(target_team):
    """Loop through data files and collect only the match IDs that have a certain team in it
    and return a dictionary of lists that contains the matches that the team played as either radiant or dire
    
    Collect the matches from the dict by: dict['radiant'/'dire']"""

    target_team = "VGJ Storm"

    target_matches = defaultdict(list)

    # simple version for working with CWD
    for match in [name for name in os.listdir('{:}/{:}'.format(path, game_version))]:
        with open('{:}/{:}/{:}'.format(path, game_version, match),'r') as outfile:
            data = json.load(outfile)
        try:
            if data['pro_team_data'][2]['radiant_name'] == target_team:
                target_matches["radiant"].append(match)
            if data['pro_team_data'][4]['dire_name'] == target_team:
                target_matches["dire"].append(match)
        except:
            continue

    return(target_matches)
