from flask import Blueprint, make_response
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
