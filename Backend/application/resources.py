from flask_restful import Resource
from .extensions import security, db
from .utils import output, validate_token, evaluate_submission, code_dir, export_chat
from flask_restful import fields, marshal, reqparse
from flask_security import auth_required, current_user, roles_required, roles_accepted
from .models import User, Course, Submission, CourseMaterial, Chat
import json
from flask import request, url_for
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from datetime import datetime
from sqlalchemy import desc
from .sample_agent import chatbot, fetch_history
from .sample_admin import upload_file, delete_file, update_file

user_datastore = security.datastore

crntdir = str(Path(os.path.abspath(os.path.dirname(__file__))).parents[0])
static_dir = crntdir + '/static'

course_fields = {
    'id': fields.Integer,
    'name': fields.String
}

# Course Api
class CourseApi(Resource) :

    @auth_required('token')
    @validate_token()
    def get(self, id=None) :
        courses = current_user.courses
        if not id :
            if courses :
                data = {'courses': marshal(courses, course_fields)}
                return output(200, 'Courses fetched successfully', data)
            else :
                return output(404, 'You have not enrolled to any course')
        else :
            if courses :
                for course in courses :
                    if course.id == id:
                        data = {'course': marshal(course, course_fields)}
                        data['course']['content'] = course.content
                        if current_user.roles[0].name == 'student' :
                            return output(200, 'Course fetched successfully', data)
                        else :
                            return output(402, 'You are not allowed to access that resource')
                return output(404, f'You have not enrolled to the course with id {id}')
            else :
                return output(404, 'You have not enrolled to any course')

submission_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'score': fields.Integer
}

submission_parser = reqparse.RequestParser()
submission_parser.add_argument('assignment_id')
submission_parser.add_argument('content')

# Submission Api
class SubmissionApi(Resource) :

    @auth_required('token')
    @validate_token()
    @roles_required('student')
    def get(self, id):
        submission = Submission.query.filter_by(user_id=current_user.id, assignment_id=id).order_by(desc(Submission.id)).first()
        if submission :
            data = {'submission': marshal(submission, submission_fields)}
            return output(200, 'Submission fetched successfully', data)
        else :
            return output(404, 'You haven\'t made any submission yet')


    @auth_required('token')
    @validate_token()
    @roles_required('student')
    def post(self) :
        # getting the data
        submission_data = submission_parser.parse_args()

        assignment_id = submission_data['assignment_id']
        try :
            content = json.loads(submission_data['content'])
        except:
            content = submission_data['content']

        # verify if the assignment exists
        data = assignment_id.split('-')

        # verify enrollment
        course_id = int(data[0])
        flag = False
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                break

        if not flag :
            return output(404, 'Course not found')

        course_content = json.loads(Course.query.filter_by(id=course_id).first().content)

        section_id = int(data[1])
        item_id = int(data[2])

        flag = False
        for section in course_content :
            if section['id'] == section_id :
                for item in section['items'] :
                    if item['id'] == item_id :
                        result = evaluate_submission(item, content)

                        submission = Submission(
                            user_id=current_user.id, 
                            assignment_id=assignment_id, 
                            content=json.dumps(result['content']),
                            score=result['points']
                            )

                        db.session.add(submission)
                        db.session.commit()

                        flag = True
                        break
                if not flag :
                    return output(404, 'Assignment not found')
        if not flag :
            return output(404, 'Assignment not found')

        return output(200, 'Submission made successfully', result)

material_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'type': fields.String,
    'path': fields.String
}

# Materials Api
class MaterialApi(Resource) :

    @auth_required('token')
    @validate_token()
    @roles_accepted('ta', 'instructor')
    def get(self, course_id) :

        # check for enrollment
        flag = False
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                break
        if not flag :
            return output(402, 'You have not enrolled to the course')

        materials = CourseMaterial.query.filter_by(course_id=course_id).all()

        if not materials :
            return output(404, 'No course materials found')

        data = {'materials': marshal(materials, material_fields)}

        return output(200, 'Course Materials fetched successfully', data)


    @auth_required('token')
    @validate_token()
    @roles_accepted('ta', 'instructor')
    def post(self, course_id) :

        # check for enrollment
        flag = False
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                break
        if not flag :
            return output(402, 'You have not enrolled to the course')


        title = request.form['title']
        file_type = request.form['type']
        file = request.files['file']

        if (file.filename == '') or (not title) or (not file_type) :
            return output(403, 'Missing input fields')


        filename = secure_filename(str(title) + '.' + file.filename.split('.')[-1])
        file.save(os.path.join(static_dir + '/uploads/', filename))

        material = CourseMaterial(
                user_id=current_user.id,
                course_id=course_id,
                title=title,
                type=file_type,
                path=url_for('static', filename='uploads/' + filename),
                vector_id=10 # <- To be modified
            )

        db.session.add(material)
        db.session.commit()

        upload_file(os.path.join(static_dir + '/uploads/', filename), course_id, title)

        return output(200, 'Material uploaded successfully')

    @auth_required('token')
    @validate_token()
    @roles_accepted('ta', 'instructor')
    def put(self, course_id) :

        # check for enrollment
        flag = False
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                break
        if not flag :
            return output(402, 'You have not enrolled to the course')

        id = request.form['id']
        title = request.form['title']
        file_type = request.form['type']
        file = request.files['file']

        if (not id) or (not title) or (not file_type):
            return output(403, 'Missing input fields')

        material = CourseMaterial.query.filter_by(id=id,course_id=course_id).first()

        if not material :
            return output(404, 'Material not found')

        old_title = material.title
        material.title = title
        material.type = file_type

        if file :
            os.remove(crntdir + material.path)
            filename = secure_filename(str(title) + '.' + file.filename.split('.')[-1])
            file.save(os.path.join(static_dir + '/uploads/', filename))

            material.path = url_for('static', filename='uploads/' + filename)
            material.vector_id = 20 # <- to be modified
            
        db.session.commit()

        update_file(crntdir + material.path, course_id, old_title, title)
        
        return output(200, 'Material edited successfully')

    @auth_required('token')
    @validate_token()
    @roles_accepted('ta', 'instructor')
    def delete(self, course_id, material_id) :

        # check for enrollment
        flag = False
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                break
        if not flag :
            return output(402, 'You have not enrolled to the course')

        material = CourseMaterial.query.filter_by(id=material_id,course_id=course_id).first()

        if not material :
            return output(404, 'Material not found')

        os.remove(crntdir + material.path)

        db.session.delete(material)    
        db.session.commit()
        
        delete(course_id, material.title)
        
        return output(200, 'Material deleted successfully')

# Temporary in-memory chat storage
chat_history = dict()

chat_fields = {
    'id': fields.Integer,
    'time': fields.DateTime(dt_format='rfc822'),
    'session_id': fields.String
}

chat_parser = reqparse.RequestParser()
chat_parser.add_argument('query')
chat_parser.add_argument('tag')
chat_parser.add_argument('chat_id')
chat_parser.add_argument('resources')
chat_parser.add_argument('code')

# ChatOutline Api
class ChatOutlineApi(Resource) :

    @auth_required('token')
    @validate_token()
    @roles_accepted('student')
    def get(self, course_id) :

        # check for enrollment
        flag = False
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                break
        if not flag :
            return output(402, 'You have not enrolled to the course')

        chats = Chat.query.filter_by(user_id=current_user.id, course_id=course_id).all()

        if not chats :
            return output(404, 'No chats found')

        data = marshal(chats, chat_fields)

        return output(200, 'Chats fetched successfully', data)

    @auth_required('token')
    @validate_token()
    @roles_accepted('student')
    def post(self, course_id) :
        data = chat_parser.parse_args()
        query = data['query']
        tag = data['tag']
        resources = data['resources']
        code = data['code']

        # check for enrollment
        flag = False
        c = None
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                c = json.loads(course.content)
                break
        if not flag :
            return output(402, 'You have not enrolled to the course')

        if not query or not tag :
            return output(403, 'Missing input fields')

        # parsing tag
        pars = [int(x) for x in tag.split('-')]
        if not len(pars) == 1:
            if len(pars) > 3 :
                course_id, section_id, content_id, question_id = pars
            elif :
                course_id, section_id, content_id = pars

            flag = False
            context=None
            for section in c :
                if section['id'] == section_id :
                    for item in section['items'] :
                        if item['id'] == content_id :
                            context = item['type']
                            flag = True
                            break
                if flag :
                    break
            if not flag :
                return output(403, 'Invalid Tag')

        if context in ['lecture', 'practice-assignment', 'graded-assignment'] :
            response = chatbot(
                context,
                tag,
                query,
                resources=resources
            )
        elif context == 'programming-assignment' :
            response = chatbot(
                context,
                tag,
                query,
                code= code,
                resources=resources
            )
        else :
            response = chatbot(
                'course',
                tag,
                query
                resources=resources
            )

        time_stamp = datetime.now()
        chat = Chat(user_id=current_user.id, course_id=course_id, time=time_stamp, session_id=response['session_id'])

        db.session.add(chat)
        db.session.commit()

        return output(200, 'Chat Created successfully', {'message': response['message'], 'session_id': response['session_id']})

# ChatApi
class ChatApi(Resource) :

    @auth_required('token')
    @validate_token()
    @roles_accepted('student')
    def get(self, course_id, session_id) :

        # check for enrollment
        flag = False
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                break
        if not flag :
            return output(402, 'You have not enrolled to the course')

        chat = Chat.query.filter_by(course_id=course_id, session_id=session_id, user_id=current_user.id).first()

        if not chat :
            return output(404, 'Chat history not found')

        return output(200, 'Chat history fetched successfully', {"chat": fetch_history(session_id)})


    @auth_required('token')
    @validate_token()
    @roles_accepted('student')
    def post(self, course_id, session_id) :
        data = chat_parser.parse_args()
        query = data['query']
        tag = data['tag']
        resources = data['resources']
        code = data['code']

        # check for enrollment
        flag = False
        c = None
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                c = json.loads(course.content)
                break
        if not flag :
            return output(402, 'You have not enrolled to the course')

        if not query or not tag :
            return output(403, 'Missing input fields')

        # parsing tag
        pars = [int(x) for x in tag.split('-')]
        if not len(pars) == 1:
            if len(pars) > 3 :
                course_id, section_id, content_id, question_id = pars
            elif :
                course_id, section_id, content_id = pars

            flag = False
            context=None
            for section in c :
                if section['id'] == section_id :
                    for item in section['items'] :
                        if item['id'] == content_id :
                            context = item['type']
                            flag = True
                            break
                if flag :
                    break
            if not flag :
                return output(403, 'Invalid Tag')


        chat = Chat.query.filter_by(course_id=course_id, session_id=session_id, user_id=current_user.id).first()

        if not chat :
            return output(404, 'Chat history not found')

        if context in ['lecture', 'practice-assignment', 'graded-assignment'] :
            response = chatbot(
                context,
                tag,
                query,
                resources=resources,
                session_id=session_id
            )
        elif context == 'programming-assignment' :
            response = chatbot(
                context,
                tag,
                query,
                code= code,
                resources=resources,
                session_id=session_id
            )
        else: 
            response = chatbot(
                'course',
                tag,
                query,
                resources=resources,
                session_id=session_id
            )

        return output(200, 'Message added successfully', {'message': response['message'], 'session_id': session_id})

    @auth_required('token')
    @validate_token()
    @roles_accepted('student')
    def delete(self, course_id, session_id) :

        # check for enrollment
        flag = False
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                break
        if not flag :
            return output(402, 'You have not enrolled to the course')

        chat = Chat.query.filter_by(course_id=course_id, session_id=session_id, user_id=current_user.id).first()

        if not chat :
            return output(404, 'Chat history not found')

        db.session.delete(chat)
        db.session.commit()

        return output(200, 'Chat history deleted successfully')

    @auth_required('token')
    @validate_token()
    @roles_required('student')
    def put(self, course_id, session_id) :
        
        # check for enrollment
        flag = False
        for course in current_user.courses :
            if course.id == course_id :
                flag = True
                break
        if not flag :
            return output(402, 'You have not enrolled to the course')

        chat = Chat.query.filter_by(course_id=course_id, session_id=session_id, user_id=current_user.id).first()

        if not chat :
            return output(404, 'Chat history not found')
        path = export_chat(fetch_history(session_id), session_id)

        return output(200, 'Chat exported successfully', {'path': path})
