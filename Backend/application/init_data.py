import os
from pathlib import Path
from flask_security import hash_password
from .models import Course, Enrollment
from .extensions import db

crntdir = str(Path(os.path.abspath(os.path.dirname(__file__))).parents[0])
static_dir = crntdir + '/static'

# init roles and student
def init_data(user_datastore) :

    # Populating Roles
    user_datastore.find_or_create_role(
        name='student',
        description='The main user of the SEEK portal'
    )
    user_datastore.find_or_create_role(
        name='ta',
        description='student with additional functionality'
    )
    user_datastore.find_or_create_role(
        name='instructor',
        description='course instructor'
    )

    # creating a dummy Student
    if not user_datastore.find_user(username='dummy_student') :
        user_datastore.create_user(
            username='dummy_student',
            password=hash_password('password'),
            roles=['student']
        )
    
    # creating a dummy TA
    if not user_datastore.find_user(username='dummy_ta') :
        user_datastore.create_user(
            username='dummy_ta',
            password=hash_password('password'),
            roles=['ta']
        )

    # since ta is also a student
    # creating a seperate student account for the ta
    if not user_datastore.find_user(username='dummy_student_2') :
        user_datastore.create_user(
            username='dummy_student_2',
            password=hash_password('password'),
            roles=['student']
        )

    # creating a dummy Instructor
    if not user_datastore.find_user(username='dummy_instructor') :
        user_datastore.create_user(
            username='dummy_instructor',
            password=hash_password('password'),
            roles=['instructor']
        )

    # commit changes
    user_datastore.commit()

    # Creating course
    course = Course.query.filter_by(name="Programming in Python").first()
    if not course :
        content = ''
        with open(static_dir + '/course-1.json', 'r') as f :
            content = f.read()
        course = Course(name="Programming in Python", content=content)
        db.session.add(course)

    # Creating Enrollment
    for i in range(1, 5) :
        enrollment = Enrollment.query.filter_by(user_id=i).first()
        if not enrollment:
            enrollment = Enrollment(user_id=i, course_id=1)
            db.session.add(enrollment)

    # commiting changes
    db.session.commit()
