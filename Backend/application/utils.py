from functools import wraps
from flask_security import current_user
from flask import request, url_for
from .models import Token
import subprocess
import os
from pathlib import Path
from fpdf import FPDF

crntdir = str(Path(os.path.abspath(os.path.dirname(__file__))).parents[0])
code_dir = crntdir + '/static/codes/'
export_dir = crntdir + '/static/exports'

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

    return {'points': score, 'questions': response}

# Export chat as pdf
def export_chat(history, session_id) :
    chat = history[session_id]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)

    for message in chat :
        height = len(message['message'].split('\n')) + 6
        if message['role'] == 'user' :
            pdf.cell(50)
            pdf.cell(0, height, message['message'], ln=1, align='R')
        else :
            pdf.cell(0, height, message['message'], ln=1, align='L')
        pdf.cell(0, 10, ln=1)

    pdf.output(export_dir + '/' + str(session_id) + '.pdf')

    return url_for('static', filename='exports/' + str(session_id) + '.pdf')
