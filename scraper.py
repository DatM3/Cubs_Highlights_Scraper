#!/user/bin/python

import requests
from bs4 import BeautifulSoup
import datetime
import re

# Get current date information and format it for the url
now = datetime.datetime.now()
month = str(now.month)
day = str(now.day)

if len(month) == 1:
	month = "0" + month

if len(day) == 1:
	day = "0" + day

# Form the base url using the date and search for the url specific to the Cubs game
base_url = 'http://gdx.mlb.com/components/game/mlb/year_2015/month_' + str(month) + '/day_' + str(day) + '/'
series_response = requests.get(base_url)
current_series = BeautifulSoup(series_response.text)

for element in current_series.find_all("li"):
	temp = str(element.string.strip())
	if "chnmlb" in temp: break

# Form the full url to access highlights
index_url = base_url + temp + 'media/highlights.xml'

#Use BeautifulSoup to parse the highlights xml
highlights_response = requests.get(index_url)
current_highlights = BeautifulSoup(highlights_response.text, "xml")

# Error check if there are no highlights
# To do: Make a seperate error message for games that have not started
if "[]" in str(current_highlights.find_all(team_id = "112")):
	print("There are no highlights yet!")

# Search by team_id to filter by Cubs highlights only
for element in current_highlights.find_all(team_id = "112"):
	# Print out highlight name and direct url to highlight
	#To do: save highlight information to an output file
	print(str(element.blurb.string) + ": " + str(element.url.string))
