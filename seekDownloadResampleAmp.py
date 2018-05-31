# add database storing the podcast which were already downloaded (and therefore
# already heard)
# from sys import platform
import sys
import os
dir2store = "/media/%s/"%(os.environ['LOGNAME'])
if sys.platform == "darwin":
	dir2store = "/Volumes/"
dir2store = "%sSANDISK SAN/PODCASTS/naturePodcasts/"%(dir2store)

# delete the podcasts which were already listened otherwise the list grows exponentially
# make the list
if len(sys.argv) <= 1:
	print "old files kept"
else:
	filesList = [f for f in os.listdir(dir2store)
							 if (f.endswith('.mp3') and not f.startswith('.'))]
	# delete the files
	from subprocess import call
	for fileName in filesList:
		rc = call(["rm", "%s%s" % (dir2store, fileName)])
	print "old files deleted"

import sqlite3
conn = sqlite3.connect("%sdownloadedMp3.sqlite" % (dir2store))
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS mp3
             (id INTEGER NOT NULL PRIMARY KEY,
             title TEXT UNIQUE,
             date datetime
             );
             ''')

try:
  import requests
  from bs4 import BeautifulSoup
  url = 'https://www.nature.com/nature/articles?type=nature-podcast'
  # could be easier to scrape this: 'http://rss.acast.com/nature'
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
  req = requests.get(url, headers = headers)
  soup = BeautifulSoup(req.text, "html.parser")
  links2podcasts = soup.findAll('h3', {'class':'mb10 extra-tight-line-height'})
  # figure out how many podcast are there already, this is to know what the starting value is for the 
  # counter of podcasts which were already included
  c.execute("SELECT COUNT(*) FROM mp3") # returns a line too much
  counter = c.fetchone()[0]
  startCounter = counter
  for go2podcasts in links2podcasts:
		newpage = ("https://www.nature.com%s" % go2podcasts.find('a')['href'])
		thisPage_req = requests.get(newpage, headers = headers)
		thisPage_soup = BeautifulSoup(thisPage_req.text, "html.parser")
		thisPage_links = thisPage_soup.findAll('a', href=True)
		divBody = thisPage_soup.find('div', {'class':'article__body serif cleared'})
		almostMp3 = divBody.findAll('a', href=True)
		for mp3Loc in almostMp3:
			if (mp3Loc.find("i").getText().encode('utf-8') == 'Download this episode') or (mp3Loc.find("i").getText().encode('utf-8') == 'Download mp3') :
				mp3fileLoc = mp3Loc.attrs['href']
				mp3file = requests.get(mp3fileLoc, headers = headers).content
				locDate = 4
				dateVal = mp3fileLoc.split('/')[locDate]
				locDate = 0
				currentDate = dateVal.split('-')[0]
				fileName = "nature-%s.mp3" % currentDate
				c.execute("INSERT  OR IGNORE INTO mp3(title, date) VALUES (?, datetime('now','localtime'))",
							(fileName,))
				c.execute('SELECT COUNT(*) FROM mp3')
				newCounter = c.fetchone()[0]
				if ( newCounter <= counter) :
					print "%s already downloaded" % fileName
				else:
					print "adding %s to collection" % fileName
					fileName = "%s%s" % (dir2store, fileName)
					with open(fileName,'wb') as output:
						output.write(mp3file)
					# add tags because in the new version of mp3 they aren't present
					from subprocess import call
					rc = call(["id3v2", "-t", "Nature: %s" % currentDate, "%s" % fileName])
					rc = call(["id3v2", "-TIT2", "Nature: %s" % currentDate, "%s" % fileName])
					rc = call(["id3v2", "-a", "Nature", "%s" % fileName])
					rc = call(["id3v2", "-TPE1", "Nature", "%s" % fileName])
					rc = call(["id3v2", "-A", "Nature Podcast", "%s" % fileName])		
					rc = call(["id3v2", "-TALB", "Nature Podcast", "%s" % fileName])
					counter = counter + 1
		if (counter-startCounter) > 5:
			break
except Exception as e:
  print(str(e))

conn.commit()
conn.close()
