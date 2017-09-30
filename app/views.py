from app import app
import schedule
import time

htmlheader = """
<html>
    <body>
"""
htmlfooter = """
    </body>
</html>
"""

@app.route('/')
@app.route('/index')
def index():
    strbuffer = ""
    strbuffer += htmlheader
    for programme in schedule.parse_schedule(time.strftime("%Y/%m/%d")):
        strbuffer += "<h2>" + programme[1] + "</h2>"
        pinfo = schedule.parse_programme(programme[0])
        if pinfo != None:
            tracks = pinfo.split('\n')
            for track in tracks:
                strbuffer += "<h3>"+ track + "</h3>"
    strbuffer += htmlfooter
    return strbuffer
