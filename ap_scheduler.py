from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date
from config import Config
from dusk import Dusk
from lights import Lights
import logging
from time import sleep
import sys


class LightSchedule():

    def __init__(self, lights):
        self.lights = lights


    def main(self, config, dusk):
        
        # initialize scheduler with your preferred timezone
        self.scheduler = BackgroundScheduler({
            'apscheduler.timezone': config.TIMEZONE
            })
        self.scheduler.start()

        # Look up today's dusktime 
        todayDuskDateTime = dusk.getDuskTime(date.today())
        logging.warning("** - today's sunset at: " + str(todayDuskDateTime))

        # Schedule to turn the lights on today at dusk
        job = self.scheduler.add_job(
            self.lightsOn, 
            misfire_grace_time=86400, 
            trigger='date', 
            next_run_time=str(todayDuskDateTime),
            args=[config]
        )
        logging.warning("scheduled job added: %s" % job)
        logging.warning("misfire_grace_time: " + str(job.misfire_grace_time) )

        # If it's after dusk, the scheduled job will recognize that it's 
        # been missed and turn the lights on immediately and schedule the 
        # lights to go off at the time set in config.  If's after the lights
        # off time, both the lights-on and lights-off job will be executed 
        # immediately leaving the lights in the off state.

        while True:
            sleep(60)
            sys.stdout.write('.'); sys.stdout.flush()



    def lightsOn(self, config ):
        # Turn the lights on
        logging.warning('********** Lights On *************')
        self.lights.switch('one', True)

        # Schedule to turn the lights off at time set in config
        currentDateTime = datetime.now()  #config.LIGHTS_OFF_TIME
        lightsOffList = config.LIGHTS_OFF_TIME.split(":")
        lightsOffDateTime = currentDateTime.replace(hour=int(lightsOffList[0]), minute=int(lightsOffList[1]))
        logging.warning('** - lights off time: ' + str(lightsOffDateTime))

        job = self.scheduler.add_job(
            self.lightsOff, 
            misfire_grace_time=86400, 
            trigger='date', 
            next_run_time=str(lightsOffDateTime),
            args=[config, Dusk(config)]
        )
        logging.warning("scheduled job added: %s" % job)


    def lightsOff(self, config, dusk ):
        # Turn the lights off
        logging.warning('********** Lights Off *************')
        self.lights.switch('one', False)

        # Look up tomorrow's dusktime 
        tomorrow = date.today() + timedelta(days=1)
        tomorrowDuskDateTime = dusk.getDuskTime(tomorrow)
        logging.warning('** - dusk time at: ' + str(tomorrowDuskDateTime))

        # Schedule to turn the lights on at the next dusktime
        job = self.scheduler.add_job(
            self.lightsOn, 
            misfire_grace_time=86400,
            trigger='date', 
            next_run_time=str(tomorrowDuskDateTime),
            args=[config]
        )
        logging.warning("scheduled job added: %s" % job)


    

if __name__ == "__main__":
    LightSchedule(Lights(Config())).main(Config(), Dusk(Config()))
