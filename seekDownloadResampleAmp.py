import requests
from bs4 import BeautifulSoup
import os
# add functionality to include file manually downloaded

# add database storing the podcast which were already downloaded (and therefore
# already heard)

import sqlite3
#conn = sqlite3.connect("%sdownloadedMp3.db" % (dir2store))
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
  url = 'http://www.nature.com/nature/podcast/archive.html'
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
  req = requests.get(url, headers = headers)
  soup = BeautifulSoup(req.text, "html.parser")
  links = soup.findAll('a')
  c.execute("SELECT COUNT(*) FROM mp3") # return a line too much
  counter = c.fetchone()[0]
  startCounter = counter
  for tmp in links:
		if 'mp3' in tmp.text.encode('utf-8'):
			# I don't really like futures, so I get rid of them
			if 'futures' in tmp['href'].encode('utf-8'):
				print "by-passing %s" % tmp['href'].encode('utf-8')
				continue # this does not work if using tmp.text.encode('utf-8')
			linkName = tmp['href'].encode('utf-8')
			fileName = linkName.rsplit('/', 1)[-1]
			print fileName
			c.execute("INSERT  OR IGNORE INTO mp3(title, date) VALUES (?, datetime('now','localtime'))",
						 (fileName,))
			c.execute('SELECT COUNT(*) FROM mp3')
			newCounter = c.fetchone()[0]
			if ( newCounter <= counter) :
				print "%s already downloaded" % fileName
				continue
			else:
				print "adding %s to collection" % fileName
				mp3file = requests.get(tmp['href'], headers = headers).content
				with open("%s%s" % (dir2store, fileName),'wb') as output:
					output.write(mp3file)
				counter = counter + 1
		if (counter-startCounter) > 5:
			break
except Exception as e:
  print(str(e))

conn.commit()
conn.close()
