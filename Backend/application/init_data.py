from flask_security import hash_password

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
            roles=['student', 'ta']
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
