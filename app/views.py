from app import app
import schedule
import time
import json

htmlheader = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
    </head>
 <!-- Latest compiled and minified CSS -->
 <link rel="stylesheet"
 href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

 <!-- jQuery library -->
 <script
 src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

 <!-- Latest compiled JavaScript -->
 <script
 src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <body>
        <div class="container">
"""
htmlfooter = """
        </div">
    </body>
</html>
"""

@app.route('/')
@app.route('/index')
def index():
    strbuffer = ""
    strbuffer += htmlheader
    currentSchedule = schedule.bbc6schedule('2017/10/02')
    currentSchedule.parse_schedule()
    for programme in currentSchedule.parse_schedule():
        currentSchedule.parse_programme(programme[0],programme[1])
    jsonstr = json.loads(currentSchedule.get_json())

    for programme in jsonstr['programmes']:
        strbuffer += "<h2>" + programme + "</h2>"
        for track in jsonstr['programmes'][programme]['tracks']:
            strbuffer += "<h3>%s, %s</h3>" % (track[0], track[1])
    strbuffer += htmlfooter
    return strbuffer
