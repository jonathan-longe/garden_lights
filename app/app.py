import pytz
from flask import Flask
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date
from lights import Lights
from astral import Astral
import logging

# initialize lights
lights = Lights(Config)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize scheduler with your preferred timezone
    scheduler = BackgroundScheduler({'apscheduler.timezone': Config.TIMEZONE})

    # Look up today's dusk time
    today_dusk_dt = get_today_dusk_datetime(Config.MAJOR_NEARBY_CITY, date.today())
    logging.warning("** - today's sunset at: " + str(today_dusk_dt))

    # Schedule to turn the lights on today at dusk
    job = scheduler.add_job(
        lights_on,
        misfire_grace_time=Config.MISFIRE_GRACE_TIME,
        trigger='date',
        next_run_time=today_dusk_dt,
        args=[Config.MAJOR_NEARBY_CITY, Config.LIGHTS_OFF_TIME, lights, scheduler]
    )
    logging.warning("scheduled job added: %s" % job)
    logging.warning("misfire_grace_time: " + str(job.misfire_grace_time))

    scheduler.start()

    # If it's after dusk, the scheduled job will recognize that it's
    # been missed and turn the lights on immediately and schedule the
    # lights to go off at the time set in config.  If it's after the lights
    # off time, both the lights-on and lights-off job will be executed
    # immediately leaving the lights in the off state.

    from routes import bp
    app.register_blueprint(bp)

    return app


def lights_on(major_nearby_city, light_off_time: str, local_lights, local_scheduler):
    # Turn the lights on
    logging.warning('********** Lights On *************')
    local_lights.switch('one', True)

    # Schedule to turn the lights off at time set in config
    tz = pytz.timezone(Config.TIMEZONE)
    current_dt = datetime.now(tz)  # config.LIGHTS_OFF_TIME
    lights_off_list = light_off_time.split(":")
    lights_off_dt = current_dt.replace(hour=int(lights_off_list[0]), minute=int(lights_off_list[1]))
    logging.warning('** - lights off time: ' + str(lights_off_dt))

    job = local_scheduler.add_job(
        lights_off,
        misfire_grace_time=Config.MISFIRE_GRACE_TIME,
        trigger='date',
        next_run_time=lights_off_dt,
        args=[major_nearby_city, light_off_time, local_lights, local_scheduler]
    )
    logging.warning("scheduled job added: %s" % job)


def lights_off(major_nearby_city, lights_off_time, local_lights, local_scheduler):
    # Turn the lights off
    logging.warning('********** Lights Off *************')
    local_lights.switch('one', False)

    # Look up tomorrow's dusk time
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_dusk_dt = get_today_dusk_datetime(major_nearby_city, tomorrow)
    logging.warning('** - dusk time at: ' + str(tomorrow_dusk_dt))

    # Schedule to turn the lights on at the next dusk time
    job = local_scheduler.add_job(
        lights_on,
        misfire_grace_time=Config.MISFIRE_GRACE_TIME,
        trigger='date',
        next_run_time=tomorrow_dusk_dt,
        args=[major_nearby_city, lights_off_time, local_lights, local_scheduler]
    )
    logging.warning("scheduled job added: %s" % job)


def get_today_dusk_datetime(closest_major_city_name: str, today_date: date) -> datetime:
    astral = Astral()
    astral.solar_depression = 'civil'
    location = astral[closest_major_city_name]
    sun = location.sun(today_date, True)
    return sun['dusk']
