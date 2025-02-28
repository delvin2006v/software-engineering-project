from flask_restful import Resource
from .extensions import security
from .utils import output
from flask_restful import fields, marshal
from .models import User

user_datastore = security.datastore

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
}

# User Api
class UserApi(Resource) :

    def get(self, id=None) :
        if id :
            user = user_datastore.find_user(id=id)
            if user :
                data = {'user': marshal(user, user_fields)}
                return output(200, 'User fetched successfully', data)
            else :
                return output(404, 'User not found')
        else :
            users = User.query.all()
            if users :
                data = {'users': [marshal(user, user_fields) for user in users]}
                return output(200, 'Users fetched successfully', data)
