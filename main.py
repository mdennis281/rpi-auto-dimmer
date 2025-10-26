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
    
    consecutive_errors = 0
    max_retries = 3
    
    while True:
        try:
            idle_time = idle_monitor.idle_seconds()

            if idle_time > DIM_DELAY_SECONDS:
                sc.brightness = IDLE_BRIGHTNESS
                logger.info("Idle for %.1fs: Dimming screen to %d%%", idle_time, IDLE_BRIGHTNESS)
            else:
                sc.brightness = ACTIVE_BRIGHTNESS
                logger.debug("Active for %.1fs: Setting screen to %d%%", idle_time, ACTIVE_BRIGHTNESS)

            # Reset error counter on successful operation
            consecutive_errors = 0
            time.sleep(CHECK_INTERVAL)
            
        except (OSError, IOError, ValueError) as e:
            consecutive_errors += 1
            logger.error("Error in main loop (attempt %d/%d): %s", consecutive_errors, max_retries, e)
            logger.error("Traceback: \n", exc_info=True)
            
            if consecutive_errors >= max_retries:
                logger.critical("Maximum retry attempts (%d) reached. Service shutting down.", max_retries)
                logger.critical("Check hardware connections and system configuration.")
                raise e
            
            # Exponential backoff: 1s, 2s, 4s
            retry_delay = min(2 ** (consecutive_errors - 1), 4)
            logger.warning("Retrying in %ds...", retry_delay)
            time.sleep(retry_delay)


if __name__ == "__main__":
    main()