import RPi.GPIO as GPIO
from config import Config


class Lights():


    def __init__(self, config ):
        self.relays = config.RELAYS
        self._initializeGPIO(self.relays)
        self.reverseLogic = config.REVERSE_LOGIC
        

    def on(self, channel: str):
        GPIO.output(self.relays[channel], self._reverseLogic(self.reverseLogic, True))
        return

    def off(self, channel: str):
        GPIO.output(self.relays[channel], self._reverseLogic(self.reverseLogic, False))
        return

    def switch(self, channel: str, state: bool):
        GPIO.output(self.relays[channel], self._reverseLogic(self.reverseLogic, state))
        return

    def status(self, channel: str) -> bool:
        return self._reverseLogic(self.reverseLogic, bool(GPIO.input(self.relays[channel])))

    def _reverseLogic(self, isReversed: bool, status) -> bool:
        if(isReversed):
            return not status
        return status

    def _initializeGPIO(self, relays: dict):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        #TODO - Add foreach loop here
        GPIO.setup(relays["one"], GPIO.OUT)
        GPIO.setup(relays["two"], GPIO.OUT)
        GPIO.setup(relays["three"], GPIO.OUT)
        #TODO - End foreach loop here`

