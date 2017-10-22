import urllib2
import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import pprint
import json
import sys
import re

class bbc6schedule:
    def __init__(self, date):
        self._schedule = {'date':date, 'programmes':{}}
        self._baseurl = 'http://www.bbc.co.uk/6music/programmes/schedules/'

    def get_html(self, url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read()

        return html

    def parse_schedule(self):
        resourcere = re.compile('^.*typeof=\"RadioEpisode\" resource=\"(?P<resource>http://[^\"]+)\".*?name\">(?P<show>[^<]+).*')

        url = self._baseurl + self._schedule['date']
        print 'DEBUG:parse_schedule %s' % (url)
        html = self.get_html(url)

        soup = BeautifulSoup.BeautifulSoup(html)

        shows = []
        for tag in soup.findAll(resource=True,typeof="RadioEpisode"):
            match =  resourcere.match(str(tag))
            if match:
                self._schedule['programmes'][match.group('show')] = {
                    'url':match.group('resource'),
                    'tracks':[]}
                shows.append((match.group('resource'),match.group('show')))

        return shows

    def parse_programme(self,programmeurl,programme):
        strbuffer = ""
        try:
            url = programmeurl + '/segments.inc'
            html = self.get_html(url)

            soup = BeautifulSoup.BeautifulSoup(html)
            #s = soup.findAll('span','artist')
            s = soup.findAll('div')
            for tag in s:
                for attr in tag.attrs:
                    if 'data-title' in attr:
                        (artist,track) = attr[1].replace(' || ','||').split('||')
                        self._schedule['programmes'][programme]['tracks'].append((artist,track))
                        strbuffer += attr[1] + "\n"
        except Exception as e:
            print 'exception %s\n', e

    def get_json(self):
        return json.dumps(self._schedule)

    def worker_mp(self,inputs):
        self.parse_programme(inputs[0], inputs[1])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "%s Usage: %s" % (sys.argv[0], "date <YYYY/MM/DD>")
        sys.exit(1)

    schedule = bbc6schedule(sys.argv[1]) 
    data = schedule.parse_schedule()
    p = ThreadPool(len(data))
    p.map(schedule.worker_mp, data)


    #for programme in schedule.parse_schedule():
    #    schedule.parse_programme(programme[0],programme[1])
    #for key in schedule._schedule['programmes']:
    #    print key
    #    for programme in schedule._schedule['programmes'][key]['tracks']:
    #        print programme[0], programme[1]

    data = json.loads(schedule.get_json())

    for key in data['programmes']:
        print key
        for track in data['programmes'][key]['tracks']:
            print 'artist: %s song: %s' % (track[0], track[1])
