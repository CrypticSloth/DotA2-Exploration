# Test File
# V 1.0.0

import requests
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import sys
from current_dota_version import current_dota_version
import time

path = 'F:/DataSets/versions'
current_time = datetime.now().strftime('%m/%d/%Y %H:%M')

# Current version of dota right now
game_version = current_dota_version() #version grabbed from dota2.gamepedia.com/GameVersion

# Check to see if the version path exists. If it doesnt, create a new version path and work in that directory
version_path = Path('{:}/{:}'.format(path, game_version))

def Parser():
	"Grabs dota data from the opendota API, adds some useful information to it, and stores it in the correct directory based on the version of dota the game was played in"

	# Grab Pro matches from opendota.api
	page = requests.get('https://api.opendota.com/api/proMatches')
	games = page.content

	# Load the json file
	proMatches = json.loads(games)

	# Grab match id for each of the pro matches
	match_id = []
	for i in range(len(proMatches)):
		match_id.append(proMatches[i]['match_id'])

	# Download each of the matches into their own json files and store them to disk
	for match in match_id:
		match_page = requests.get('https://api.opendota.com/api/matches/{:}'.format(match))
		match_details = match_page.content
		match_details = json.loads(match_details)
		with open('{:}/{:}/{:}.json'.format(path, game_version, match),'w') as outfile:
			json.dump(match_details, outfile)
		time.sleep(1)

	counter = 0
	# Add Pro Team information and date collected to each match
	for match in match_id:
		# Open each matches data
		with open('{:}/{:}/{:}.json'.format(path, game_version, match),'r') as outfile:
			data = json.load(outfile)
		# Add the information that we want to the file
		data['pro_team_data'] = [{'match_id':proMatches[counter]['match_id']},{'radiant_team_id':proMatches[counter]['radiant_team_id']},{'radiant_name':proMatches[counter]['radiant_name']},{'dire_team_id':proMatches[counter]['dire_team_id']},{'dire_name':proMatches[counter]['dire_name']},{'league_id':proMatches[counter]['leagueid']},{'league_name':proMatches[counter]['league_name']}]
		data['date_collected'] = current_time
		counter += 1
		# Save the file back to disk
		with open('{:}/{:}/{:}.json'.format(path, game_version, match),'w') as outfile:
			json.dump(data, outfile)

	# Replace match version num with our version
	for match in match_id:
		# Open each matches data
		with open('{:}/{:}/{:}.json'.format(path, game_version, match),'r') as outfile:
			data = json.load(outfile)
		# Add the new information
		data['version'] = game_version
		# Save to disk
		with open('{:}/{:}/{:}.json'.format(path, game_version, match),'w') as outfile:
			json.dump(data, outfile)

	return

# Save match to their appropriate game version file
# If file does not exist then create a new one
try:
	if version_path.is_dir():
		#Coninue
		Parser()
	else:
		version_path.mkdir()
		#Continue
		Parser()
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
