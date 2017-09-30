import urllib2
import BeautifulSoup
import pprint
import sys
import re


def parse_schedule(date):
    baseurl = 'http://www.bbc.co.uk/6music/programmes/schedules/'
    resourcere = re.compile('^.*typeof=\"RadioEpisode\" resource=\"(?P<resource>http://[^\"]+)\".*?name\">(?P<show>[^<]+).*')

    req = urllib2.Request(baseurl + date)
    response = urllib2.urlopen(req)

    html = response.read()
    soup = BeautifulSoup.BeautifulSoup(html)

    shows = []
    for tag in soup.findAll(resource=True,typeof="RadioEpisode"):
        match =  resourcere.match(str(tag))
        if match:
            shows.append((match.group('resource'),match.group('show')))
            #print match.group('resource')
            #print match.group('show')

    return shows

def parse_programme(programme):
    print programme + '/segments.inc'
    strbuffer = ""
    try:
        req = urllib2.Request(programme + '/segments.inc')
        response = urllib2.urlopen(req)
        html = response.read()
        soup = BeautifulSoup.BeautifulSoup(html)
        #s = soup.findAll('span','artist')
        s = soup.findAll('div')
        for tag in s:
            for attr in tag.attrs:
                if 'data-title' in attr:
                    #print(attr[1])
                    strbuffer += attr[1] + "\n"
    except:
        print "can't load programme ",programme

    return strbuffer


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "%s Usage: %s" % (sys.argv[0], "date <YYYY/MM/DD>")
        sys.exit(1)

    for programme in parse_schedule(sys.argv[1]):
        #print programme
        parse_programme(programme[0])