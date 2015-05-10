#!/user/bin/python

import requests
from bs4 import BeautifulSoup
import datetime

# Get current date information
now = datetime.datetime.now()

# Get the url for the current gameday highlights (I need to figure out how to account for series changes still)
index_url = 'http://gdx.mlb.com/components/game/mlb/year_2015/month_0' + str(now.month) + '/day_0' + str(now.day) + '/gid_2015_0' + str(now.month) + '_0' + str(now.day) + '_chnmlb_milmlb_1/media/highlights.xml'

# Use BeautifulSoup to parse the highlights xml
response = requests.get(index_url)
soup = BeautifulSoup(response.text, "xml")

# Search by team_id to filter by Cubs highlights only
for element in soup.find_all(team_id = "112"):
	# Print out highlight name and direct url to highlight
	# Still need to save highlight information to an output file
	print(str(element.blurb.string) + ": " + str(element.url.string))


