This Repo contains all of my analysis and content that I have done working with Dota Analysis. It contains some scripts for collecting data from the Opendota.com API as well as the Stratz API. It also contains some of my ad hoc analysis of the data. So far I have started to work on some market basket analysis trying to analyze drafts, as well as some analysis based on if there is a correlation between number of wards placed and winrate. Feel free to contact me if you have any suggestions on any more Ad Hocs that might be useful/interesting.


**My Scripts**

My scripts first get the current dota version from [GamePedia](gamepedia.com/Game_Versions "GamePedia.com") using the BeautifulSoup package in Python.

Then it grabs the data from the last 100 *Professional* dota matches using the [opendota API](docs.opendota.com). These matches are considered professional based on if the game is part of a tournament with money prizes.

In another script, I add more data that is grabbed from the [stratz API](docs.stratz.com) that captures every event. This includes player positions and everything they do at every point in the game. I am hoping to do some movement and ward placement analysis of certain professional teams in the future.

When it grabs this data it puts it in its appropriate version folder based on the current version found from gamepedia. Also adds some useful information like date collected, current version (in a readable format), the two team names that played that game, and the tournament the game was played in.

The data is in json format.

I have made this run every night on my Windows computer using Task Scheduler. I have been collecting pro matches since patch 7.07d. If you would like some of this data you can email me at sorensen.erik48@gmail.com

**Analysis**

This folder contains all of my Ad Hoc analysis. I try to keep things as published as possible but this is a constant work in progress so things will sometimes be unfinished/not in a clean or published state.