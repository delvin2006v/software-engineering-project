from flask import Flask
from application.config import LocalConfig, TestConfig
from application.extensions import db, security
from application.init_data import init_data
from flask_restful import Api
from flask_cors import CORS
import sys

app, api = None, None

# Init Flask app
def create_app(for_test=False) :
    app = Flask(__name__)
    if for_test :
        app.config.from_object(TestConfig)
    else :
        app.config.from_object(LocalConfig)
    CORS(app,resources={r"/*": {"origins": "*"}})

    api = Api(app)
    db.init_app(app)

    with app.app_context() :
        from application.models import User, Role
        from flask_security import SQLAlchemyUserDatastore

        user_datastore = SQLAlchemyUserDatastore(db, User, Role)

        security.init_app(app, user_datastore)
        if for_test :
            db.drop_all()
            db.create_all()
        else :
            db.create_all()
        init_data(user_datastore)

    app.app_context().push()

    return (app, api)

n = len(sys.argv)
if n > 1 and sys.argv[1] == 'test' :
    app, api = create_app(True)
else :
    app, api = create_app()

# importing views
from application.views import *

# importing api
from application.resources import CourseApi, SubmissionApi, MaterialApi, ChatOutlineApi, ChatApi

api.add_resource(CourseApi, '/courses/<int:id>', '/courses')
api.add_resource(SubmissionApi, '/submissions/<string:id>', '/submissions')
api.add_resource(MaterialApi, '/courses/<int:course_id>/materials', '/courses/<int:course_id>/materials/<int:material_id>')
api.add_resource(ChatOutlineApi, '/chats/<int:course_id>')
api.add_resource(ChatApi, '/chats/<int:course_id>/<int:session_id>')

# start dev server
if __name__ == '__main__' :
    app.run()
