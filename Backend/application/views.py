from flask import current_app as app
from flask import request
from .extensions import security, db
from .utils import output, validate_token
from flask_security import hash_password, auth_required, current_user, verify_password
from .models import Token

user_datastore = security.datastore

# ping
@app.route('/', methods=['GET'])
@auth_required('token')
@validate_token()
def ping() :
    return output(200,'Server is up !')

# Login route
@app.route('/user_login', methods=['POST'])
def user_login() :
    ''' Checks User credinals and provides an Authentication-Token '''
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # verify inputs
    if (not username) or (not password) :
        return output(401, 'Missing input fields')

    # verify existance of the User
    user = user_datastore.find_user(username=username)

    # account not found
    if not user :
        return output(404, f'User account with username {username} does not exists')

    # verify password
    if not verify_password(password, user.password) :
        return output(403, 'Incorrect Password')

    # get token
    gen_token = user.get_auth_token()

    # output data
    data = {
        'id': user.id,
        'username': user.username,
        'role': user.roles[0].name,
        'token': gen_token
    }

    # storing the token
    token = Token.query.filter_by(user_id=user.id).first()
    if token :
        # replacing old token
        token.token = gen_token
    else :
        # creating a new record
        token = Token(user_id=user.id, token=gen_token)
        db.session.add(token)

    # commiting changes
    db.session.commit()

    return output(200, "Logged in successfully", data)

# Logout route
@app.route('/user_logout', methods=['POST'])
@auth_required('token')
@validate_token()
def user_logout() :
    ''' Deleting existing record '''
    token = Token.query.filter_by(user_id=current_user.id).first()

    # since validate_token checks whether the record exists
    # we need not check it here

    db.session.delete(token)
    db.session.commit()

    return output(200, 'Logout successfully.')

