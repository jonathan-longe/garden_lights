
from config import Config
from astral import Astral
from datetime import date
import logging


class Dusk():    

    def __init__(self, majorCityName: str):
        self.majorCityName = majorCityName
        self.astral = Astral()
        logging.warning(majorCityName)


    def getCurrentDuskTime(self):
        self.astral.solar_depression = 'civil'
        location = self.astral[self.majorCityName]
        d = date.today()
        sun = location.sun( d, True )

        return str(sun['dusk'])
        
