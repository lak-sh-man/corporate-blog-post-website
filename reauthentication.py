# purpose of this function is to avoid user accessing un authenticated pages like 
# user accessing admin pages and admin accessing user pages after oneself gets authenticated 
# this function helps in achieving authorization via authentication

from functools import wraps
from flask import redirect, url_for, request, session, flash
from flask_login import current_user

def reauth_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('reauthenticated'):
                flash('Please re-authenticate to access this page.', 'warning')
                if role == 'user' and current_user.id != 0:
                    return redirect(url_for('admin_authentication_bp.admin_login', next=request.url))
                elif role == 'admin' and current_user.id == 0:
                    return redirect(url_for('user_authentication_bp.user_login', next=request.url))
            return f(*args, **kwargs)
        return decorated_function
    return decorator