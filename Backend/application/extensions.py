from flask_sqlalchemy import SQLAlchemy
from flask_security import Security

security = Security()
db = SQLAlchemy()

# Output in JSON
def output(code, msg, data=None) :
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
