import time
from src import idle_monitor
from src.screen_control import ScreenControl
from src.helpers import setup_logging, load_config
from src.decorator import retry_on_exception

# Set up logging and configuration  
logger = setup_logging()
IDLE_BRIGHTNESS, ACTIVE_BRIGHTNESS, DIM_DELAY_SECONDS, CHECK_INTERVAL = load_config()

@retry_on_exception(max_retries=5, delay=5)
def initialize_screen_control():
    return ScreenControl()

def main():
    logger.info("Starting Raspberry Pi Auto-Dimmer service")
    logger.info("Configuration: Idle brightness=%d%%, Active brightness=%d%%, Delay=%ds", 
                IDLE_BRIGHTNESS, ACTIVE_BRIGHTNESS, DIM_DELAY_SECONDS)

    # Initialize screen control safely
    sc = initialize_screen_control()

    while True:
        main_loop(sc)


@retry_on_exception(max_retries=3, delay=1)
def main_loop(sc: ScreenControl):
    idle_time = idle_monitor.idle_seconds()
    last_brightness = sc.brightness

    # sc.set_brightness returns True if brightness was changed
    if idle_time > DIM_DELAY_SECONDS:
        if sc.set_brightness(IDLE_BRIGHTNESS):
            logger.info(
                "Idle for %.1fs: Dimming screen to %d%% (current %d%%)", 
                idle_time, IDLE_BRIGHTNESS, last_brightness
                )
    else:
        if sc.set_brightness(ACTIVE_BRIGHTNESS):
            logger.debug(
                "Active for %.1fs: Setting screen to %d%% (current %d%%)", 
                idle_time, ACTIVE_BRIGHTNESS, last_brightness
                )
    time.sleep(CHECK_INTERVAL)



if __name__ == "__main__":
    main()