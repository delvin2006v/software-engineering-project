from flask import request, url_for
from functools import wraps
from flask_security import current_user
from .models import Token
from .extensions import security
import subprocess
import os
from pathlib import Path
from fpdf import FPDF

crntdir = str(Path(os.path.abspath(os.path.dirname(__file__))).parents[0])
code_dir = crntdir + '/static/codes/'
export_dir = crntdir + '/static/exports'


# unauth handler
def unauth_handler(mechanics=None, headers=None) :
    return output(401, 'Authentication Failed')

security.unauthn_handler(unauth_handler)

# unauthz handler
def unauthz_handler(func, params=None) :
    return output(402, 'You are not allowed to access that resource')

security.unauthz_handler(unauthz_handler)

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

# Assignment Evaluation function
def evaluate_submission(key, response) :
    score = 0
    if key['type'] in ['practice-assignment', 'graded-assignment'] :
        for i in range(len(key['questions'])) :
            flag = True
            qn = key['questions'][i]
            res = response[i]
            cnt = 0
            for opt in res['option'] :
                if opt not in qn['answer'] :
                    flag = False
                    break
                else :
                    cnt += 1
            if flag :
                response[i]['correct'] = 1
                score += (qn['points']/len(qn['answer']))*cnt
            else :
                response[i]['correct'] = 0
    elif key['type'] == 'programming-assignment' :

        # saving user code
        with open(code_dir + 'student_code.py', 'w') as f :
            f.write(response)
            
        res = key['cases'].copy()
        cases = key['cases']
        for i in range(len(key['cases'])) :
            output = subprocess.run(
                ['python', code_dir + 'student_code.py'],
                input=cases[i]['input'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if output.stdout.strip() == cases[i]['output'] :
                score += 1
                res[i]['pass'] = 1
            else :
                res[i]['pass'] = 0
            res[i]['output'] = output.stdout + output.stderr
            response = {'code': response, 'cases': res}

    return {'points': score, 'content': response}

# Export chat as pdf
def export_chat(history, session_id) :
    chat = history
    html_str = '''<style>#chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.message {
  width: fit-content;
  max-width: 70%;
  margin: 10px 0;
  padding: 10px 16px;
  border-radius: 15px;
  position: relative;
  border: 1px solid black;
}

.incoming {
  background: #f1f1f1;
  margin-right: auto;
  color: black
}

.outgoing {
  background: #0084ff;
  color: white;
  margin-left: auto;
}

.timestamp {
  display: block;
  font-size: 0.75rem;
  opacity: 0.8;
  margin-top: 4px;
}

/* Markdown content styling within messages */
.message .content h1 {
  font-size: 1.2rem;
  margin: 5px 0;
}

.message .content ul {
  padding-left: 20px;
}
</style><div id="chat-container">'''

    for message in chat :
        align = 'incoming'
        if message['role'] == 'user' :
            align = 'outgoing'
        html_str += (f'<div class="message {align}"><div class="content">' + message['message'] + '</div></div>')
    html_str += '</div>'
    print(export_dir)

    with open(export_dir + '/' + str(session_id) + '.html', 'w') as f:
        f.write(html_str)
        f.close()

    return url_for('static', filename='exports/' + str(session_id) + '.html')
