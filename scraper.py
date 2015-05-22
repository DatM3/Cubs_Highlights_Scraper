#!/user/bin/python

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Begin definitons of functions #

# Finds the series URL specific to the Cubs game
def find_series (series_obj):
	for element in series_obj.find_all('li'):
		series = str(element.string.strip())
		if 'chnmlb' in series: return series

# Parses and converts the start time of the game to CT
def get_start_time (game_info_obj):
	# Get the game time and convert it to CT (Time zone Cubs play in)
	game_time = "%s%s" % (game_info_obj.game['time'], game_info_obj.game['ampm'])
	time_format = "%s-%s-%s %s" % (year, month, day, game_time)
	time_zone = "CT"
	start_time_CT = datetime.strptime(time_format, "%Y-%m-%d %I:%M%p")
	return start_time_CT.replace(hour = start_time_CT.hour - 1)

# Parses the team's name and record
def get_team_info(team, game_info_obj):
	team_name = "%s_team_name" % team
	wins = "%s_win" % team
	loss = "%s_loss" % team
	return "%s (%s-%s)" % (game_info_obj.game[team_name], game_info_obj.game[wins], game_info_obj.game[loss])

# Prints/writes to file an error message if there are no highlights for the Cubs
def error_check (current_highlights, now, start_time):
	if "[]" in str(current_highlights.find_all(team_id = '112')):
		if (now < start_time):
			print("The game hasn't started yet!")
			file.write("The game hasn't started yet!")
		else:
			print("The game is in progress, but we don't have any highlights yet!")
			file.write("The game is in progress, but we don't have any highlights yet!")

# Parse only highlights from the Cubs and prints them to console/writes them to file
def get_highlights (current_highlights):
	for element in current_highlights.find_all(team_id = '112'):
		# Print out and save highlight name and direct url to highlight
		highlight_string = "%s: %s\n" % (element.blurb.string, element.url.string)
		print(highlight_string)
		file.write("%s\n" % (highlight_string))

# End definition of functions #

# Begin main script #

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

# Find the Cubs series URL
base_url = "http://gdx.mlb.com/components/game/mlb/year_2015/month_%s/day_%s/" % (month, day)
series_response = requests.get(base_url)
series_obj = BeautifulSoup(series_response.text)
current_series = find_series(series_obj)

# Form the URL used to parse gameday information
game_url = "%s%slinescore.xml" % (base_url, current_series)
game_response = requests.get(game_url)
game_info_obj = BeautifulSoup(game_response.text, 'xml')

# Parse the starting time and team info
start_time = get_start_time (game_info_obj)
time_zone = "CT"
away = get_team_info('away', game_info_obj)
home = get_team_info('home', game_info_obj)

# Print/write to file the gameday info
print("Gameday:\n%s/%s %s @ %s %s %s\n" % (month, day, away, home, start_time.strftime("%I:%M%p"), time_zone))
file.write("Gameday:\n%s/%s %s @ %s %s %s\n\n" % (month, day, away, home, start_time.strftime("%I:%M%p"), time_zone))

# Form the URL used to parse the highlights
index_url = "%s%smedia/highlights.xml" % (base_url, current_series)
highlights_response = requests.get(index_url)
current_highlights = BeautifulSoup(highlights_response.text, 'xml')

# Print/write to file all the available Cubs highlights
print("Highlights:")
file.write("Highlights:\n")
error_check(current_highlights, now, start_time)
get_highlights(current_highlights)

file.close()

# End main script #