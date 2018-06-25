# Web Page parser to grab Dota version
from bs4 import BeautifulSoup
import requests

def current_dota_version():
	page = requests.get('https://dota2.gamepedia.com/Game_Versions')
	data = page.text
	soup = BeautifulSoup(data,'lxml')
	version_links = soup.find_all('a', class_='mw-redirect')

	versions = []
	for row in version_links:
	    versions.append(row['title'])

	cleaned_versions = []
	for i in versions:
	    try:
	        if (type(int(i[0]))) == int:
	            cleaned_versions.append(i)
	    except:
	        continue

	current_version = cleaned_versions[0]
	return(current_version)