from flask import Flask
from application.config import LocalConfig
from application.extensions import db, security
from application.init_data import init_data
from flask_restful import Api

app, api = None, None

# Init Flask app
def create_app() :
    app = Flask(__name__)
    app.config.from_object(LocalConfig)
    api = Api(app)
    db.init_app(app)

    with app.app_context() :
        from application.models import User, Role
        from flask_security import SQLAlchemyUserDatastore

        user_datastore = SQLAlchemyUserDatastore(db, User, Role)

        security.init_app(app, user_datastore)
        db.create_all()
        init_data(user_datastore)

    app.app_context().push()

    return (app, api)

app, api = create_app()

# importing views
from application.views import *

# importing api
from application.resources import UserApi

api.add_resource(UserApi, '/api/users/<int:id>', '/api/users')

# start dev server
if __name__ == '__main__' :
    app.run()
