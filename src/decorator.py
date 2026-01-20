import time
import threading
from functools import wraps
from src.helpers import setup_logging

log = setup_logging(__name__)

def threaded(daemon=False):
    """
    Decorator that runs the decorated function in a separate thread.
    
    Args:
        daemon (bool): Whether the thread should be a daemon thread. Default is False.
    
    Returns:
        threading.Thread: The thread object that was started.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=daemon)
            thread.start()
            return thread
        return wrapper
    return decorator


def retry_on_exception(max_retries=3, delay=2):
    """
    Decorator that retries the decorated function on specified exceptions.
    
    Args:
        max_retries (int): Maximum number of retries. Default is 3.
        delay (int): Delay in seconds between retries. Default is 2.
        exceptions (tuple): Tuple of exception classes to catch for retries. Default is (Exception,).
    
    Returns:
        The return value of the decorated function if successful.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    log.warning("Exception in %s: %s (attempt %d/%d)", func.__name__, e, attempts, max_retries)
                    if attempts >= max_retries:
                        log.error("Max retries reached for %s. Raising exception.", func.__name__)
                        raise e
                    log.info("Retrying %s in %d seconds...", func.__name__, delay)
                    time.sleep(delay)
        return wrapper
    return decorator