import threading
from functools import wraps


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