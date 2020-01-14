#!/usr/bin/python

from flask import request, jsonify
from flask_api import FlaskAPI
import RPi.GPIO as GPIO

RELAYS = {"one": 37, "two": 38, "three": 40}
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(RELAYS["one"], GPIO.OUT)
GPIO.setup(RELAYS["two"], GPIO.OUT)
GPIO.setup(RELAYS["three"], GPIO.OUT)

app = FlaskAPI(__name__)

@app.route('/relays/', methods=["GET"])
def api_root():
    array = []
    for channel in ["one","two","three"]:
      array.append({ 
          'channel': channel,
          'state':  bool(GPIO.input(RELAYS[channel]))
          })
    return array

  
@app.route('/relays/<channel>/', methods=["GET", "POST"])
def api_relays_control(channel):
    if request.method == "POST":
        if channel in RELAYS and "state" in request.data:
            GPIO.output(RELAYS[channel], int(request.data.get("state")))

        if channel in RELAYS and "toggle" in request.data:
            GPIO.output(RELAYS[channel], not GPIO.input(RELAYS[channel]))

    return { 
             'channel': channel,
             'state': bool(GPIO.input(RELAYS[channel]))
           }

if __name__ == "__main__":
    app.run(debug=True)

