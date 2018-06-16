Dota Analysis README.txt

First grabs the current dota version from gamepedia.com/Game_Versions using BeautifulSoup

Then grabs the data of the last 100 pro dota matches using the opendota api.

When it grabs this data it puts it in its appropriate version folder based on the current version found from gamepedia. Also adds some useful information like date collected, current version (in a readable format), the two team names that played that game, and the tournament the game was played in.

The data is in json format.

*********************************************

Future Analysis Ideas:
	Movement analysis on teams to find patterns in there movement
		Find out what strategy works best for the current meta (splitpush, 5 manning, etc.)
		Maybe find new movement strats with unsupervised learning
			Thoughts:
				Use the two features (time and location) and for every second plot those on map (probably whole team)
				Since the data is in two dimensions we can easily graph and run unsupervised learning to group the movements of the team.
				When the movements are grouped we can look at it and identify some common movements that teams do.
					Maybe even map these movements onto a dota map for easy identification and visualization (woudld be neat for a final visualization report)
	Relation to number of wards placed and winrate in lower mmr games (where sometimes few wards will be placed in a game)
	Some kind of draft analysis, find what heros play together the best etc using machine learning
		Maybe first just find the team comps that have the highest avg winrate
		Association rules (apriori)
	Relationship between toxic chatting and winrate

	Analysing certain teams patterns.
		-Sneaky Ward Placements 
		-Smoke Timings