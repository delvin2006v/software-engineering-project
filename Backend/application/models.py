from .extensions import db
from flask_security import UserMixin, RoleMixin
from flask_security.models import fsqla_v3 as fsq

fsq.FsModels.set_db_info(db)

# User Model
class User(db.Model, UserMixin) :
    ''' Stores the User details '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    fs_uniquifier = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary='roles_users')
    courses = db.relationship('Course', secondary='enrollment')

# Role Model
class Role(db.Model, RoleMixin) :
    ''' Stores the Role details '''
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=True, nullable=False)

# Token Model
class Token(db.Model) :
    ''' Stores the latest Authentication-Token '''
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    token = db.Column(db.String, nullable=False)

# Course Model
class Course(db.Model) :
    ''' Stores the course content '''
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    content = db.Column(db.String, unique=True, nullable=False)

# Enrollment Model
class Enrollment(db.Model) :
    ''' Stores the Enrollment details of the Users '''
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    # unique constraint
    # to ensure that one user is enrolled to a course only once
    db.UniqueConstraint(user_id, course_id)

# Submission Model
class Submission(db.Model) :
    ''' Store the assignment submission of the students '''
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment_id = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)

# Chat Model
class Chat(db.Model) :
    ''' Store the chat history of the Student '''
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    session_id = db.Column(db.Integer, nullable=False, unique=True)
    time = db.Column(db.DateTime, nullable=False)
    
    # unique constraint
    # to ensure that no two records have the same user, course and session_id
    db.UniqueConstraint(user_id, course_id, session_id)

# Course Material Model
class CourseMaterial(db.Model) :
    ''' Store the course material details '''
    __tablename__ = 'coursematerial'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    vector_id = db.Column(db.Integer, nullable=False)
