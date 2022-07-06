from flask import Blueprint, make_response
from prometheus_client import Enum
from app import lights
from app import scheduler

bp = Blueprint('main', __name__, url_prefix='/api')


@bp.get("/status")
def status():
    return make_response({"is_lights_on": lights.status("one")})


@bp.get("/schedule")
def schedule():
    jobs = scheduler.get_jobs()
    if len(jobs) > 0:
        return make_response({
            "next_dt": str(jobs[0].next_run_time),
            "function": jobs[0].func.__name__
        })
    return make_response({"jobs": "none"})


@bp.get("/metrics")
def metrics():
    e = Enum('garden_lights_state', 'Are the lights on or off?',
             states=['lights-on', 'lights-off'])
    if lights.status("one"):
        return e.state('lights-on')
    return e.state('lights-off')
