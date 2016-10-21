import requests
from bs4 import BeautifulSoup
from subprocess import call
import os

dir2store = "/media/%s/SANDISK SAN/PODCASTS/naturePodcasts/"%(os.environ['LOGNAME'])

try:
  url = 'http://www.nature.com/nature/podcast/archive.html'
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
  req = requests.get(url, headers = headers)
  soup = BeautifulSoup(req.text, "html.parser")
  links = soup.findAll('a')
  counter = 0
  for tmp in links:
		if 'mp3' in tmp.text.encode('utf-8'):
			# I don't really like futures, so I get rid of them
			if 'futures' in tmp['href'].encode('utf-8'):
				print "by-passing %s" % tmp['href'].encode('utf-8')
				continue # this does not work if using tmp.text.encode('utf-8')
			linkName = tmp['href'].encode('utf-8')
			fileName = linkName.rsplit('/', 1)[-1]
			if os.path.isfile("%sc_%s" % (dir2store, fileName)):
				print "%s already downloaded" % fileName
				continue
			else:
				print "adding %s to collection" % fileName
				mp3file = requests.get(tmp['href'], headers = headers).content
				with open("%s%s" % (dir2store, fileName),'wb') as output:
					output.write(mp3file)
				# make mono	
				#rc = call(["sox", "-v", "2", "%s%s" % (dir2store, fileName), "-r", "16000", 
							 #"-c", "1", "%sc_%s" % (dir2store, fileName)])
				# keep stereo
				rc = call(["sox", "-v", "2", "%s%s" % (dir2store, fileName), "-r", "16000", 
							 "%sc_%s" % (dir2store, fileName)])
				rc = call(["rm", "%s%s" % (dir2store, fileName)])
				counter = counter + 1
		podcasts2download	= 5	
		if counter > podcasts2download:
			break
except Exception as e:
  print(str(e))
  

