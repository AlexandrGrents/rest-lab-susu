from functools import wraps

from flask import session, redirect, url_for

def logined(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('log'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper