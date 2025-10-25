import time
from src import idle_monitor
from src.screen_control import ScreenControl
from src.helpers import setup_logging, load_config

# Set up logging and configuration  
logger = setup_logging()
IDLE_BRIGHTNESS, ACTIVE_BRIGHTNESS, DIM_DELAY_SECONDS, CHECK_INTERVAL = load_config()
sc = ScreenControl()

def main():
    logger.info("Starting Raspberry Pi Auto-Dimmer service")
    logger.info("Configuration: Idle brightness=%d%%, Active brightness=%d%%, Delay=%ds", 
                IDLE_BRIGHTNESS, ACTIVE_BRIGHTNESS, DIM_DELAY_SECONDS)
    
    while True:
        try:
            idle_time = idle_monitor.idle_seconds()

            if idle_time > DIM_DELAY_SECONDS:
                sc.brightness = IDLE_BRIGHTNESS
                logger.info("Idle for %.1fs: Dimming screen to %d%%", idle_time, IDLE_BRIGHTNESS)
            else:
                sc.brightness = ACTIVE_BRIGHTNESS
                logger.debug("Active for %.1fs: Setting screen to %d%%", idle_time, ACTIVE_BRIGHTNESS)

            time.sleep(CHECK_INTERVAL)
        except (OSError, IOError, ValueError) as e:
            logger.error("Error in main loop: %s", e)
            time.sleep(1)  # Brief pause before retrying


if __name__ == "__main__":
    main()