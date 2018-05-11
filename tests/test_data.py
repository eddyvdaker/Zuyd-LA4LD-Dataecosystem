from app.models import User, Role

TEST_DATA = {
    'users': [
        {
            'username': 'admin',
            'email': 'admin@la4ld-test.com',
            'password': 'la4ld',
            'card_number': 1234,
            'role': 'admin',
            'groups': [],
            'student': [],
            'teacher': [],
            'examiner': []
        },
        {
            'username': 'student1',
            'email': 'student1@la4ld-test.com',
            'password': 'la4ld',
            'card_number': 2345,
            'role': 'student',
            'groups': [],
            'student': [],
            'teacher': [],
            'examiner': []
        },
    ],
    'roles': ['admin', 'student', 'teacher', 'system'],
    'modules': [
        {
            'code': 'tm01',
            'name': 'Test Module 01',
            'Description': 'The first testing module',
            'start': '2018-03-30',
            'end': '2018-10-30',
            'faculty': 'ict'
        },
        {
            'code': 'tm01',
            'name': 'Test Module 01',
            'Description': 'The fist testing module (last years version)',
            'start': '2017-03-30',
            'end': '2017-10-30',
            'faculty': 'ict'
        },
        {
            'code': 'tm02',
            'name': 'Test Module 02',
            'Description': 'The second testing module',
            'start': '2018-03-30',
            'end': '2018-10-30',
            'faculty': 'ict'
        },
        {
            'code': 'tm03',
            'name': 'Test Module 03',
            'Description': 'The third testing module',
            'start': '2019-03-30',
            'end': '2019-10-30',
            'faculty': 'ict'
        },
    ],
    'groups': [
        {
            'code': 'ict1',
            'active': True,
            'modules': ['tm01', 'tm03']
        },
        {
            'code': 'ict2',
            'active': True,
            'modules': ['tm02']
        },
        {
            'code': 'ict1',
            'active': False,
            'modules': ['tm01']
        }
    ],
    'schedules': [
        {
            'description': 'ict1 - tm01 schedule',
            'group': 'ict1',
            'module': 'tm01',
            'items': [
                {
                    'title': 'tm01 - WK1 LESSON 1',
                    'description': 'First lesson of tm01',
                    'start': '2018-04-01 09:30',
                    'end': '2018-04-01 10:30',
                    'room': 'B3.205'
                },
                {
                    'title': 'tm01 - WK1 LESSON 2',
                    'description': 'Second lesson of tm01',
                    'start': '2018-05-12 13:30',
                    'end': '2018-05-12 15:30',
                    'room': 'B2.221'
                }
            ]
        },
        {
            'description': 'ict1 - tm01 schedule',
            'group': 'ict1',
            'module': 'tm01',
            'items': [
                {
                    'title': 'tm01 - WK1 LESSON 1',
                    'description': 'First lesson of tm01',
                    'start': '2018-04-01 09:30',
                    'end': '2018-04-01 10:30',
                    'room': 'B3.205'
                },
                {
                    'title': 'tm01 - WK1 LESSON 2',
                    'description': 'Second lesson of tm01',
                    'start': '2018-05-12 13:30',
                    'end': '2018-05-12 15:30',
                    'room': 'B2.221'
                }
            ]
        },
    ]
}


def write_test_data_to_test_db(db, data=TEST_DATA):
    for role in TEST_DATA['roles']:
        r = Role(role=role)
        db.session.add(r)
        db.session.commit()
    for user in data['users']:
        # noinspection PyArgumentList
        u = User(
            username=user['username'],
            email=user['email'],
            card_number=user['card_number']
        )
        u.role_id = Role.query.filter_by(role=user['role']).first().id
        u.set_password(user['password'])
