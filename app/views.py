from flask import render_template
from app import app
import schedule
import time
import json

@app.route('/')
@app.route('/index')
def index():
    currentSchedule = schedule.bbc6schedule(time.strftime('%Y/%m/%d'))
    currentSchedule.parse_schedule()
    for programme in currentSchedule.parse_schedule():
        currentSchedule.parse_programme(programme[0],programme[1])
    jsonstr = json.loads(currentSchedule.get_json())

    return render_template("index.html", programmes=jsonstr)
