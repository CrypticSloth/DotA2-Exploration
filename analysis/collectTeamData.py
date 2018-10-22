# Loop through data files and collect only the match IDs that have a certain team in it
import json
import os, os.path
from tqdm import tqdm
from collections import defaultdict

def search_matches_for_team(target_team, target_versions, collect_data = True, progress_bar = False, path='../versions_test'):
    """
    Loop through data files and collect only the match IDs that have a certain team in it
    and return a dictionary of lists that contains the matches that the team played under either radiant or dire
    
    Inputs:
        target_team - the team you are collecting match id's for. (make sure you are typing in the name exactly, it is case-sensitive)
        target_versions - a list of the versions the game was played in that you want to collect ids for. eg: ['7.18','7.19','7.19a']
        progress_bar - True if you want to display a progress bar, False if not (default)
        path - The location of your data from your current directory. Default is ../versions_test

    Returns:
        Dictionary of lists
        Collect the matches from the dict by: dict['radiant'/'dire']
    
    This function assumes your path looks something like this:
    ../versions_test/dota_versions/data.json

    Make it have two options, one to either return a list of ids of games the target team played in, or return a list of the actual games data
    """

    target_matches = defaultdict(list)
    target_data = defaultdict(list)

    if collect_data == True:
        if progress_bar == True:
            for version in target_versions:
                for match in tqdm([name for name in os.listdir('{:}/{:}'.format(path, version))],desc="gathering data from version {:}".format(version)):
                    with open('{:}/{:}/{:}'.format(path, version, match),'r') as outfile:
                        data = json.load(outfile)
                    try:
                        if data['radiant_team']['name'] == target_team: 
                            target_data['radiant'].append(data)
                        if data['dire_team']['name'] == target_team:
                            target_data['radiant'].append(data)
                    except:
                        continue  
            return(target_data)

        if progress_bar == False:
            for version in target_versions:
                for match in [name for name in os.listdir('{:}/{:}'.format(path, version))]:
                    with open('{:}/{:}/{:}'.format(path, version, match),'r') as outfile:
                        data = json.load(outfile)
                    try:
                        if data['radiant_team']['name'] == target_team: 
                            target_data["radiant"].append(data)
                        if data['dire_team']['name'] == target_team:
                            target_data["dire"].append(data)
                    except:
                        continue
            return(target_data)

    else: 
        if progress_bar == True:
            for version in target_versions:
                for match in tqdm([name for name in os.listdir('{:}/{:}'.format(path, version))],desc="gathering data from version {:}".format(version)):
                    with open('{:}/{:}/{:}'.format(path, version, match),'r') as outfile:
                        data = json.load(outfile)
                    try:
                        if data['radiant_team']['name'] == target_team: 
                            target_matches["radiant"].append(match)
                        if data['dire_team']['name'] == target_team:
                            target_matches["dire"].append(match)
                    except:
                        continue  
            return(target_matches)

        if progress_bar == False:
            for version in target_versions:
                for match in [name for name in os.listdir('{:}/{:}'.format(path, version))]:
                    with open('{:}/{:}/{:}'.format(path, version, match),'r') as outfile:
                        data = json.load(outfile)
                    try:
                        if data['radiant_team']['name'] == target_team: 
                            target_matches["radiant"].append(match)
                        if data['dire_team']['name'] == target_team:
                            target_matches["dire"].append(match)
                    except:
                        continue
            return(target_matches)

if __name__ == '__main__':

    target_team = "Evil Geniuses"
    target_versions = ["7.18"]
    matches = search_matches_for_team(target_team,target_versions,progress_bar=True)
    print(matches)