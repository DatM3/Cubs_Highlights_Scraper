#!/user/bin/python

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Get current date information
now = datetime.now()
month = str(now.month)
day = str(now.day)
year = str(now.year)

# Format the month and day appropriately
if len(month) == 1:
	month = "0%s" % (month)

if len(day) == 1:
	day = "0%s" % (day)

# Create a file to save highlights to 
file_string = "highlights_%s_%s.txt" % (month, day)
file = open(file_string, 'w')

# Form the base url and search for the url specific to the Cubs game
base_url = "http://gdx.mlb.com/components/game/mlb/year_2015/month_%s/day_%s/" % (month, day)
series_response = requests.get(base_url)
current_series = BeautifulSoup(series_response.text)

for element in current_series.find_all('li'):
	series = str(element.string.strip())
	if 'chnmlb' in series: break

# Form the gameday url and parse the gameday info
game_url = "%s%slinescore.xml" % (base_url, series)
game_response = requests.get(game_url)
game_info = BeautifulSoup(game_response.text, 'xml')

# Get the starting time and team info
game_time = "%s%s" % (game_info.game['away_time'], game_info.game['away_ampm'])
time_zone = "%s" % game_info.game['away_time_zone']
away = "%s (%s-%s)" % (game_info.game['away_team_name'], game_info.game['away_win'], game_info.game['away_loss'])
home = "%s (%s-%s)" % (game_info.game['home_team_name'], game_info.game['home_win'], game_info.game['home_loss'])

# Print and save gameday info
print("Gameday:\n%s/%s %s @ %s %s %s\n" % (month, day, away, home, game_time, time_zone))
file.write("Gameday:\n%s/%s %s @ %s %s %s\n\n" % (month, day, away, home, game_time, time_zone))

# Form the highlights url and parse the highlights
index_url = "%s%smedia/highlights.xml" % (base_url, series)
highlights_response = requests.get(index_url)
current_highlights = BeautifulSoup(highlights_response.text, 'xml')

print("Highlights:")
file.write("Highlights:\n")

# Error check if there are no highlights
if "[]" in str(current_highlights.find_all(team_id = '112')):
	# Create a datetime object to compare times
	time_format = "%s-%s-%s %s" % (year, month, day, game_time)
	start_time = datetime.strptime(time_format, "%Y-%m-%d %I:%M%p")

	if (now < start_time):
		print("The game hasn't started yet!")
		file.write("The game hasn't started yet!")
	else:
		print("The game is in progress, but we don't have any highlights yet!")
		file.write("The game is in progress, but we don't have any highlights yet!")

# Search by team_id to filter by Cubs highlights only
for element in current_highlights.find_all(team_id = '112'):
	# Print out and save highlight name and direct url to highlight
	highlight_string = "%s: %s\n" % (element.blurb.string, element.url.string)
	print(highlight_string)
	file.write("%s\n" % (highlight_string))

file.close()