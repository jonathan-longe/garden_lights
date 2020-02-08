from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date
from dateutil import parser
from config import Config
from dusk import Dusk
#from lights import Lights
import logging

class LightSchedule():

    def __init__(self, config, dusk, lights):
        # initialize scheduler with your preferred timezone
        self.dusk = dusk,
        self.lights = lights,
        self.config = config,
        self.scheduler = BackgroundScheduler({'apscheduler.timezone': config.TIMEZONE})
        self.scheduler.start()


    def main(self, config):
        # Lookup today's dusktime 
        # If it's not yet dusktime, schedule lights to turn on today at dusk

        currentDateTime = datetime.now()  #config.LIGHTS_OFF_TIME
        lightsOffList = config.LIGHTS_OFF_TIME.split(":")
        
        lightsOffDateTime = currentDateTime.replace(hour=int(lightsOffList[0]), minute=int(lightsOffList[1]))
        logging.warning('** - lights off at: ' + str(lightsOffDateTime))

        # If it's past dusktime, schedule the lights to turn on tomorrow at dusk
        



    def lightsOn(self, lights, config ):
        # Turn the lights on
        logging.warning('********** Lights On *************')

        # Schedule to turn the lights off at time set in config
        lightOffDateTime = config.LIGHTS_OFF_TIME 
        job = self.scheduler.add_job(self.lightsOff, trigger='date', next_run_time=str(date_time),
                                args=[self.lights, self.config])
        logging.warning("job details: %s" % job)


    def lightsOff(self, lights, config ):
        # Turn the lights off
        logging.warning('********** Lights Off *************')

        # Look up tomorrow's dusktime 

        # Schedule to turn the lights on at the next dusktime
        job = self.scheduler.add_job(self.lightsOn, trigger='date', next_run_time=str(date_time),
                                args=[self.lights, self.config])
        logging.warning("job details: %s" % job)




    def printing_something(text):
            print("printing %s at %s" % (text, datetime.now()))


if __name__ == "__main__":
    LightSchedule(Config(), Dusk(Config()), Dusk(Config()) ).main(Config())
