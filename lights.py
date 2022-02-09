import RPi.GPIO as GPIO


class Lights:

    def __init__(self, config):
        self.relays = config.RELAYS
        self._initialize_gpio(self.relays)
        self.reverseLogic = config.REVERSE_LOGIC

    def on(self, channel: str):
        GPIO.output(self.relays[channel], self._reverse_logic(self.reverseLogic, True))
        return

    def off(self, channel: str):
        GPIO.output(self.relays[channel], self._reverse_logic(self.reverseLogic, False))
        return

    def switch(self, channel: str, state: bool):
        GPIO.output(self.relays[channel], self._reverse_logic(self.reverseLogic, state))
        return

    def status(self, channel: str) -> bool:
        return self._reverse_logic(self.reverseLogic, bool(GPIO.input(self.relays[channel])))

    @staticmethod
    def _reverse_logic(is_reversed: bool, status) -> bool:
        if is_reversed:
            return not status
        return status

    @staticmethod
    def _initialize_gpio(relays: dict):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(relays["one"], GPIO.OUT)
        GPIO.setup(relays["two"], GPIO.OUT)
        GPIO.setup(relays["three"], GPIO.OUT)

