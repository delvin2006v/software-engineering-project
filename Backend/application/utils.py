from functools import wraps
from flask_security import current_user
from flask import request
from .models import Token

# Output in JSON
def output(code, msg, data=None) :
    ''' Formats the input into structured JSON for the API '''
    res = {
        'status': {
            'code': code,
            'success': 1 if code == 200 else 0,
            'message': msg
        }
    }

    if data :
        res['data'] = data
    
    return res, code

# Validate token
def validate_token() :
    ''' Custom wrapper function to check validity of Authentication-Token '''
    def wrap(func) :
        @wraps(func)
        def decor_view(*args, **kwargs) :
            entry = Token.query.filter_by(user_id=current_user.id).first()
            token = request.headers.get('Authentication-Token')
            if not entry :
                return output(401, 'Please login again.')
            elif entry.token != token :
                return output(401, 'Invalid Authentication-Token provided.')
            return func(*args, **kwargs)
        return decor_view
    return wrap
