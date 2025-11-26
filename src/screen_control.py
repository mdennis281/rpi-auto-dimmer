from rpi_backlight import Backlight
from src.decorator import threaded
import time



class ScreenControl:
    def __init__(self):
        """Controls the screen backlight brightness and power state.
        
        backlight: Instance of rpi_backlight.Backlight to manage the screen backlight.
        _changing_brightness: Flag indicating if a brightness change is in progress.
        _brightness: Cached brightness level to track changes 
            (because Backlight.brightness is sketch sometimes).
        """
        self.backlight = Backlight()
        self._changing_brightness = False
        
        self._brightness: int = -1  

    @property
    def brightness(self) -> int:
        if self._brightness == -1:
            self._brightness = self.backlight.brightness
            
        return self._brightness

    @brightness.setter
    def brightness(self, brightness: int):
        if brightness != self._brightness:
            self._fade_backlight(brightness)
            self._brightness = brightness

    @property
    def power(self) -> bool:
        return self.backlight.power

    @power.setter
    def power(self, power: bool):
        self.backlight.power = power

    def set_brightness(self, brightness: int) -> bool:
        if self._changing_brightness:
            return False
        if self.brightness != brightness:
            self.brightness = brightness
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
            self.backlight.brightness = target_brightness
            self._changing_brightness = False