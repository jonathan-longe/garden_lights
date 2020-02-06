from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dateutil import parser
import logging
schedule_app = Flask(__name__)

# initialize scheduler with your preferred timezone
scheduler = BackgroundScheduler({'apscheduler.timezone': 'America/Vancouver'})
scheduler.start()



@schedule_app.route('/schedulePrint', methods=['POST'])
def schedule_to_print():
    data = request.get_json()
    #get time to schedule and text to print from the json
    datetime_string = data.get('time')
    text = data.get('text')
    
    #convert to datetime
    date_time = parser.parse(datetime_string)

    #schedule the method 'printing_something' to run the the given 'date_time' with the args 'text'
    job = scheduler.add_job(printing_something, trigger='date', next_run_time=str(date_time),
                            args=[text])
    return "job details: %s" % job


def printing_something(text):
    print("printing %s at %s" % (text, datetime.now()))