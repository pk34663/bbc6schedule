from multiprocessing.dummy import Pool as ThreadPool
from flask import render_template
from app import app
import schedule
import time
import json

@app.route('/')
@app.route('/index')
def index():
    currentSchedule = schedule.bbc6schedule(time.strftime('%Y/%m/%d'))
    data = currentSchedule.parse_schedule(currentSchedule.get_html(currentSchedule._baseurl + currentSchedule._schedule['date']))

    p = ThreadPool(len(data))
    p.map(currentSchedule.worker_mp, data)

    #for programme in currentSchedule.parse_schedule(currentSchedule.get_html(currentSchedule._baseurl + currentSchedule._schedule['date'])):
    #    currentSchedule.parse_programme(programme[0],programme[1])
    jsonstr = json.loads(currentSchedule.get_json())

    return render_template("index.html", programmes=jsonstr)
