import time

from rpi_backlight import Backlight
from src.decorator import threaded
from src.helpers import setup_logging


log = setup_logging(__name__)


class ScreenControl:
    def __init__(self):
        self.backlight = Backlight()
        self._changing_brightness = False
        self._brightness: int = -1
        # Raises OSError if firmware isn't ready; lets @retry_on_exception handle boot delays.
        self._probe_writable()

    def _probe_writable(self) -> None:
        """Raises OSError if the sysfs brightness attribute isn't writable yet."""
        self._write_brightness(self.backlight.brightness)

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
                    self._write_brightness(b)
                    time.sleep(delay)
            else:
                for b in range(current_brightness, target_brightness - 1, -step):
                    self._write_brightness(b)
                    time.sleep(delay)
            self._write_brightness(target_brightness)
        except OSError:
            log.warning("Failed to write backlight brightness (target=%d)", target_brightness, exc_info=True)
            self._brightness = -1
        finally:
            self._changing_brightness = False

    def _write_brightness(self, value: int) -> None:
        self.backlight.brightness = value