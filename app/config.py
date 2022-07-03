

class Config:
    DEBUG                   = False 
    RELAYS                  = {"one": 37, "two": 38, "three": 40}
    REVERSE_LOGIC           = False 
    MAJOR_NEARBY_CITY       = 'Vancouver'
    TIMEZONE                = 'America/Vancouver'
    LIGHTS_OFF_TIME         = '22:30'

    # The time (in seconds) how much this job’s execution is allowed to be late
    MISFIRE_GRACE_TIME      = 60 * 60 * 12
