from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def requires_role(*roles):
    """
    Decorator to restrict access to routes based on user roles.'"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator