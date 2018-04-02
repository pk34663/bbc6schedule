import urllib2
import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import requests
import pprint
import json
import sys
import re

class bbc6schedule:
    def __init__(self, date):
        self._schedule = {'date':date, 'programmes':{}}
        self._baseurl = 'http://www.bbc.co.uk/6music/programmes/schedules/'

    def get_html(self, url):
        req = requests.get(url)
        req.encoding = 'ascii'

        #req = urllib2.Request(url)
        #response = urllib2.urlopen(req)
        #html = response.read()

        return req.text

    def parse_schedule(self, html):
        soup = BeautifulSoup.BeautifulSoup(html)
        p = soup.find('script', {'type':'application/ld+json'})
        j = json.loads("".join(p).encode('ascii','ignore'))

        shows = []
        for episode in j['@graph']:
            name = ""
            if 'partOfSeries' in episode:
                name += episode['partOfSeries']['name']
            name += episode['name']
            name.encode('ascii','ignore')

            self._schedule['programmes'][name] = { 'url':episode['url'], 'tracks':[] }

            shows.append((episode['url'],name))

        return shows

    def parse_programme(self, programme, html):
        strbuffer = ""
        soup = BeautifulSoup.BeautifulSoup(html)
        s = soup.findAll('div')
        for tag in s:
            for attr in tag.attrs:
                if 'data-title' in attr:
                    (artist,track) = attr[1].replace(' || ','||').split('||')
                    artist.encode('ascii','ignore')
                    track.encode('ascii','ignore')
                    self._schedule['programmes'][programme]['tracks'].append((artist,track))
                    strbuffer += attr[1] + "\n"

    def get_json(self):
        return json.dumps(self._schedule)

    def worker_mp(self,inputs):
        url = inputs[0] + '/segments.inc'
        html = self.get_html(url)
        self.parse_programme(inputs[1], html)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "%s Usage: %s" % (sys.argv[0], "date <YYYY/MM/DD>")
        sys.exit(1)

    schedule = bbc6schedule(sys.argv[1]) 
    data = schedule.parse_schedule(schedule.get_html(schedule._baseurl + schedule._schedule['date']))
    print data
    p = ThreadPool(len(data))
    p.map(schedule.worker_mp, data)

    data = json.loads(schedule.get_json())

    for key in data['programmes']:
        print key
        for track in data['programmes'][key]['tracks']:
            print 'artist: %s song: %s' % (track[0].encode('ascii','ignore'), track[1].encode('ascii','ignore'))
