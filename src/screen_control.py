from rpi_backlight import Backlight
from src.decorator import threaded
import time



class ScreenControl:
    def __init__(self):
        self.backlight = Backlight()
        self._changing_brightness = False

    @property
    def brightness(self) -> int:
        return self.backlight.brightness

    @brightness.setter
    def brightness(self, brightness: int):
        if brightness != self.backlight.brightness:
            self._fade_backlight(brightness)

    @property
    def power(self) -> bool:
        return self.backlight.power

    @power.setter
    def power(self, power: bool):
        self.backlight.power = power

    def set_brightness(self, brightness: int) -> bool:
        if self._changing_brightness:
            return False
        if self.backlight.brightness != brightness:
            self.backlight.brightness = brightness
            return True
        return False

    @threaded(daemon=True)
    def _fade_backlight(self, target_brightness: int, step: int = 2, delay: float = 0.01):
        current_brightness = self.backlight.brightness
        self._changing_brightness = True
        try:
            if target_brightness > current_brightness:
                for b in range(current_brightness, target_brightness + 1, step):
                    self.backlight.brightness = b
                    time.sleep(delay)
            else:
                for b in range(current_brightness, target_brightness - 1, -step):
                    self.backlight.brightness = b
                    time.sleep(delay)
        finally:
            self._changing_brightness = False