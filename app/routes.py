from flask import Blueprint, make_response
from app import lights
from app import scheduler

bp = Blueprint('main', __name__)


@bp.get("/status")
def index():
    return make_response({"is_lights_on": lights.status("one")})


@bp.get("/schedule")
def index():
    jobs = scheduler.get_jobs()
    if len(jobs) > 0:
        return make_response({"jobs": str(jobs[0].next_run_time)})
    return make_response({"jobs": "none"})
