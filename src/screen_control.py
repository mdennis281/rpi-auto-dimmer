import time

from rpi_backlight import Backlight
from src.decorator import threaded
from src.helpers import setup_logging


log = setup_logging(__name__)


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

        # Probe the backlight to confirm the firmware is ready to accept
        # brightness writes. On cold boot the Pi firmware can reject mailbox
        # requests (kernel reports "Failed to write system 'brightness'
        # attribute: Invalid argument"). Constructing Backlight() does not
        # exercise a write, so without this probe the service would appear
        # healthy while every subsequent write silently failed on the
        # threaded fade worker. Raising here lets the caller's
        # @retry_on_exception back off and try again.
        self._probe_writable()

    def _probe_writable(self) -> None:
        """Write the current brightness back to itself to confirm the
        backlight sysfs attribute accepts writes. Raises OSError if the
        firmware is not ready yet."""
        current = self.backlight.brightness
        self._write_brightness(current)

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
        except OSError as e:
            # Writes to the sysfs brightness attribute can fail with EINVAL
            # when the Pi firmware is momentarily unavailable. Because this
            # runs on a daemon thread, an unhandled exception would be
            # swallowed silently and the service would appear healthy while
            # doing nothing. Log it, invalidate the cached brightness so the
            # next set_brightness call re-reads reality, and let the main
            # loop try again.
            log.warning("Failed to write backlight brightness (target=%d)", target_brightness, exc_info=True)
            self._brightness = -1
        finally:
            self._changing_brightness = False

    def _write_brightness(self, value: int) -> None:
        """Single brightness write, isolated so callers can reason about
        where OSErrors originate."""
        self.backlight.brightness = value