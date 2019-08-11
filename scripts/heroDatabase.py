import numpy as np
import pandas as pd
import json
import os

os.chdir("E:/DataSets/versions_test")

path = 'E:/DataSets/versions_test'
versions = os.listdir(path)

# Define all data we are saving
match_ids = []
patches = []
wins = []
isRadiant = []
hero_ids = []
num_kills = []
num_deaths = []
num_assists = []
num_denies = []
num_lasthits = []
golds = []
total_golds = []
total_xps = []
gpms = []
epms = []
heroDamages = []
towerDamages = []
isRandom = []
steamIds = []

for version in versions:
    matches = os.listdir(path + "/" + version)
    print(f"Aggregating data for version {version}")

    for match in matches:
        with open('{:}/{:}/{:}'.format(path, version, match),'r') as outfile:
            data = json.load(outfile)
        try:
            for player in data['players']:
                match_ids.append(match)
                patches.append(version)
                wins.append(player['win'])
                isRadiant.append(player['isRadiant'])
                hero_ids.append(player['hero_id'])
                num_kills.append(player['kills'])
                num_deaths.append(player['deaths'])
                num_assists.append(player['assists'])
                num_denies.append(player['denies'])
                num_lasthits.append(player['last_hits'])

                if type(player['gold']) != int:
                    print(player['gold'])

                golds.append(player['gold'])
                total_golds.append(player['total_gold'])
                total_xps.append(player['total_xp'])
                gpms.append(player['gold_per_min'])
                epms.append(player['xp_per_min'])
                heroDamages.append(player['hero_damage'])
                towerDamages.append(player['tower_damage'])
                steamIds.append(player['account_id'])
        except:
            continue

print(len(match_ids))
print(len(patches))
print(len(wins))
print(len(isRadiant))
print(len(hero_ids))
print(len(num_kills))
print(len(num_deaths))
print(len(num_assists))
print(len(num_denies))
print(len(num_lasthits))
print(len(golds))
print(len(total_golds))
print(len(total_xps))
print(len(gpms))
print(len(epms))
print(len(heroDamages))
print(len(towerDamages))
# print(len(isRandom))
print(len(steamIds))


# Add player information name
# Add team the game was played with 
# Add dota hero name instead of ID

df = pd.DataFrame({

    "match_id":match_ids,
    "version":patches,
    "win":wins,
    "isRadiant":isRadiant,
    "hero_id":hero_ids,
    "kills":num_kills,
    "deaths":num_deaths,
    "assists":num_assists,
    "denies":num_denies,
    "lasthits":num_lasthits,
    "gold":golds,
    "total_gold":total_golds,
    "total_xp":total_xps,
    "gold_per_min":gpms,
    "xp_per_min":epms,
    "hero_damage_dealt":heroDamages,
    "tower_damage_dealt":towerDamages,
    "account_id":steamIds
})

df.to_csv("E:/DataSets/dota_hero_dataset.csv")


# Data needed
# Most picked
# Most banned
# Highest winrate
# highest Kill average
# highest assist avg
# lowest Death avg
# highest last hit avg
# highest xpm avg
# most kills in a game
# most last hits in a game
