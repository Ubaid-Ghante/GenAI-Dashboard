from functools import wraps
import traceback

def try_and_except(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"payload": traceback.format_exc()}
    return wrapper