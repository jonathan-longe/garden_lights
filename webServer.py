from flask import request, jsonify, Response
from flask_api import FlaskAPI
#from lights import Lights
from config import Config
from dusk import Dusk

app = FlaskAPI(__name__)
#lights = Lights(Config.RELAYS, True)



# @app.route('/relays/', methods=["GET"])
# def index():
#     array = []
#     for channel in Config.RELAYS:
#       array.append({ 
#           'channel': channel,
#           'state':   lights.status(channel)
#           })
#     return array

  
# @app.route('/relays/<channel>/', methods=["PATCH"])
# def update(channel):
    
#     if channel in RELAYS and "state" in request.data:
#         lights.switch(channel, bool(request.data.get("state")))

#     if channel in RELAYS and "toggle" in request.data:
#         lights.switch(channel, not lights.status(channel))

#     return Response('updated', 204)

  
# @app.route('/relays/<channel>/', methods=["GET"])
# def show(channel):

#     return { 
#              'channel': channel,
#              'state':   lights.status(channel)
#            }


@app.route('/dusk', methods=["GET"])
def sunset():
    return Dusk(Config.MAJOR_NEARBY_CITY).getCurrentDuskTime()



if __name__ == "__main__":
    app.run(debug=True)

