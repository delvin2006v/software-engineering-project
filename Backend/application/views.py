from flask import current_app as app

# ping
@app.route('/', methods=['GET'])
def ping() :
    return 'Server is up !', 200
