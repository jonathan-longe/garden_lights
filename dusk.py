
from astral import Astral
from datetime import date
import logging


class Dusk():    

    def __init__(self, config):
        self.majorCityName = config.MAJOR_NEARBY_CITY
        self.astral = Astral()
        logging.warning('dusk initialized. Closest major city is: ' + self.majorCityName)


    def getDuskTime(self, d: date ):
        self.astral.solar_depression = 'civil'
        location = self.astral[self.majorCityName]
        sun = location.sun( d, True )

        return str(sun['dusk'])