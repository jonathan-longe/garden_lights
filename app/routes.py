from flask import Blueprint, make_response
from app import lights
bp = Blueprint('main', __name__)


@bp.get("/status")
def index():
    return make_response({"is_lights_on": lights.status("one")})

