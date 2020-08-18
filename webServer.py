from flask import request, jsonify, Response
from flask_api import FlaskAPI
from lights import Lights
from config import Config
from dusk import Dusk
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date

app = FlaskAPI(__name__)
config = Config()
lights = Lights(config)


scheduler = BackgroundScheduler({'apscheduler.timezone': config.TIMEZONE})
scheduler.start()
#job = main(config, Dusk(config))



# def main(config, dusk):
#     # Look up today's dusktime 
#     todayDuskDateTime = dusk.getDuskTime(date.today())

#     # Initial start: schedule to turn the lights on today at dusk
#     return scheduler.add_job(lightsOn, 
#         misfire_grace_time=86400, 
#         trigger='date', 
#         next_run_time=str(todayDuskDateTime),
#         args=[config]
#     )




@app.route('/relays/', methods=["GET"])
def index():
    array = []
    for channel in config.RELAYS:
      array.append({ 
          'channel': channel,
          'state':   lights.status(channel)
          })
    return array

  
@app.route('/relays/<channel>/', methods=["PATCH"])
def update(channel):
    
    if channel in config.RELAYS and "state" in request.data:
        lights.switch(channel, bool(request.data.get("state")))

    if channel in config.RELAYS and "toggle" in request.data:
        lights.switch(channel, not lights.status(channel))

    return Response('updated', 204)

  
@app.route('/relays/<channel>/', methods=["GET"])
def show(channel):

    return { 
             'channel': channel,
             'state':   lights.status(channel)
           }

@app.route('/schedule/<channel>/', methods=["POST"])
def schedule(channel):
    
    if channel in config.RELAYS and "state" in request.data:
        lights.switch(channel, bool(request.data.get("state")))

    if channel in config.RELAYS and "toggle" in request.data:
        lights.switch(channel, not lights.status(channel))

    return Response('updated', 204)


@app.route('/dusk', methods=["GET"])
def sunset():
    return Dusk(config).getDuskTime(date.today())


# Turn the lights on and schedule to turn off later
def lightsOn( config ):
    
    logging.warning('********** Lights On *************')
    lights.switch('one', True )


    # Schedule to turn the lights off at time set in config
    currentDateTime = datetime.now()  #config.LIGHTS_OFF_TIME
    lightsOffList = config.LIGHTS_OFF_TIME.split(":")
    lightsOffDateTime = currentDateTime.replace(hour=int(lightsOffList[0]), minute=int(lightsOffList[1]))
    logging.warning('** - lights off time: ' + str(lightsOffDateTime))
    job = scheduler.add_job(
        _lightsOff, 
        misfire_grace_time=86400, 
        trigger='date', 
        next_run_time=str(lightsOffDateTime),
        args=[config, Dusk(config)]
    )
    logging.warning("scheduled job added: %s" % job)

    return job






# Turn the lights off and schedule to turn on at dusk tomorrow
def lightsOff( config, dusk ):
    
    logging.warning('********** Lights Off *************')
    lights.switch('one', False)

    # Look up tomorrow's dusktime 
    tomorrow = date.today() + timedelta(days=1)
    tomorrowDuskDateTime = dusk.getDuskTime(tomorrow)
    logging.warning('** - dusk time at: ' + str(tomorrowDuskDateTime))

    # Schedule to turn the lights on at the next dusktime
    job = scheduler.add_job(
        _lightsOn, 
        misfire_grace_time=86400,
        trigger='date', 
        next_run_time=str(tomorrowDuskDateTime),
        args=[config]
    )
    logging.warning("scheduled job added: %s" % job)



if __name__ == "__main__":
    app.run(debug=True)

