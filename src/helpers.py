import logging
import configparser
import os


def setup_logging(name=__name__):
    """Configure logging for systemd service"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # This will output to systemd journal
        ]
    )
    return logging.getLogger(name)


def load_config():
    """Load configuration from config.ini file"""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
    
    # Default values
    defaults = {
        'idle_brightness': 5,
        'active_brightness': 100,
        'dim_delay_seconds': 10,
        'check_interval': 0.25
    }
    
    logger = logging.getLogger(__name__)
    
    if os.path.exists(config_path):
        try:
            config.read(config_path)
            idle_brightness = config.getint('display', 'idle_brightness', fallback=defaults['idle_brightness'])
            active_brightness = config.getint('display', 'active_brightness', fallback=defaults['active_brightness'])
            dim_delay_seconds = config.getint('display', 'dim_delay_seconds', fallback=defaults['dim_delay_seconds'])
            check_interval = config.getfloat('behavior', 'check_interval', fallback=defaults['check_interval'])
            
            logger.info("Configuration loaded from %s", config_path)
            return idle_brightness, active_brightness, dim_delay_seconds, check_interval
        except (configparser.Error, ValueError, OSError) as e:
            logger.warning("Error reading config file: %s. Using defaults.", e)
    else:
        logger.warning("Config file not found at %s. Using defaults.", config_path)
    
    return defaults['idle_brightness'], defaults['active_brightness'], defaults['dim_delay_seconds'], defaults['check_interval']