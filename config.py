import os
  
class Config():
    DEBUG                   = os.getenv('DEBUG', False )
    RELAYS                  = os.getenv('RELAYS', {"one": 37, "two": 38, "three": 40})
    REVERSE_LOGIC           = os.getenv('REVERSE_LOGIC', False )
    MAJOR_NEARBY_CITY       = os.getenv('MAJOR_NEARBY_CITY', 'Vancouver')
    TIMEZONE                = os.getenv('TIMEZONE', 'America/Vancouver')
    LIGHTS_OFF_TIME         = os.getenv('LIGHTS_OFF_TIME', '22:30')
    