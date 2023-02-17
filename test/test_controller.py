import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Flask_app.controller import controller_db
from Flask_app.models import Base, StudentModel, CourseModel, GroupModel

# зробив це для наочності, щоб показати, що для тестів я створив окрему базу даних
engine = create_engine('postgresql+psycopg2://boris:cool_pass@127.0.0.1:5432/test_db')


@pytest.fixture(scope='module')
def db_session(groups, courses):
    session = Session(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    populate_test_db(session, groups=groups, courses=courses)
    yield session

    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='module')
def courses():
    courses = (CourseModel(name='Math', description='Lorem ipsum'),
               CourseModel(name='Biology'),
               CourseModel(name='Law'))

    return courses


@pytest.fixture(scope='module')
def groups():
    groups = (GroupModel(name='FG-01'),
              GroupModel(name='DB-75'),
              GroupModel(name='CB-30'),
              GroupModel(name='GG-51'))

    return groups


def populate_test_db(session, groups, courses):
    students = []

    first_names = ('John', 'Mike', 'Desmond')
    last_names = ('Doe', 'Foo', 'Bar')

    for counter, first_name in enumerate(first_names):
        for last_name in last_names:
            students.append(StudentModel(first_name=first_name,
                                         last_name=last_name,
                                         group_name=groups[counter].name,
                                         courses=[courses[counter]])
                            )

    session.add_all([*groups, *courses, *students])
    session.commit()


class TestControllerDataBase:
    @pytest.mark.parametrize('count, expected_res', [
        (4, ['FG-01', 'DB-75', 'CB-30', 'GG-51']),
        (0, ['GG-51'])
    ])
    def test_group_less_or_equal_students(self, db_session, count, expected_res):
        with patch('Flask_app.controller.session', db_session):
            groups = controller_db.group_less_or_equal_students(count)['groups']
            names = [group['name'] for group in groups]

            assert sorted(names) == sorted(expected_res)

    def test_students_by_course_name(self, db_session):
        with patch('Flask_app.controller.session', db_session):
            students = controller_db.students_by_course_name('Biology')['students']
            students_id = [student['id'] for student in students]

            expected_res = [4, 5, 6]

        assert students_id == expected_res

    @pytest.mark.parametrize('course_name', [['Math'], [None]])
    def test_create_student(self, course_name, db_session):
        with patch('Flask_app.controller.session', db_session):
            res = controller_db.create_student(first_name='Test',
                                               last_name='Example',
                                               courses=course_name,
                                               group_name='CB-30')

            assert res

    @pytest.mark.parametrize('first_name, last_name, _courses, group_name', (
            ('Very very very long long long long name', 'Example', ['courses'], 'CB-30'),
            ('Test', 'Very very very long long long long name', ['courses'], 'CB-30'),
            ('Test', 'Very very very long long long long name', 'courses', 'CB-30'),
            ('Test', 'Very very very long long long long name', ['courses'], 'Wrong name')
    ))
    def test_create_student_error(self, db_session, first_name, last_name, _courses, group_name):
        with patch('Flask_app.controller.session', db_session):
            res = controller_db.create_student(first_name=first_name,
                                               last_name=last_name,
                                               courses=_courses,
                                               group_name=group_name)

            assert not res

    def test_delete_student(self, db_session, student_id=1):
        with patch('Flask_app.controller.session', db_session):
            res = controller_db.delete_student(student_id=student_id)

            assert res

    @pytest.mark.parametrize('student_id', ('fail', 100))
    def test_delete_student_error(self, db_session, student_id):
        with patch('Flask_app.controller.session', db_session):
            res = controller_db.delete_student(student_id=student_id)

            assert not res

    def test_add_course_to_student(self, db_session, student_id=2, course_name='Law'):
        with patch('Flask_app.controller.session', db_session):
            res = controller_db.add_course_to_student(student_id=student_id, course_name=course_name)

            assert res

    @pytest.mark.parametrize('student_id, course_name', (
            (2, 'Math'),
            (100, 'Math'),
            (2, 'Wrong_course_name')
    ))
    def test_add_course_to_student_error(self, db_session, student_id, course_name):
        with patch('Flask_app.controller.session', db_session):
            res = controller_db.add_course_to_student(student_id=student_id, course_name=course_name)

            assert not res

    def test_delete_course_from_student(self, db_session, student_id=2, course_name='Math'):
        with patch('Flask_app.controller.session', db_session):
            res = controller_db.delete_course_from_student(student_id=student_id, course_name=course_name)

            assert res

    @pytest.mark.parametrize('student_id, course_name', (
                             (2, 'Biology'),
                             (100, 'Math'),
                             (2, 'Wrong_course_name')
    ))
    def test_delete_course_from_student_error(self, db_session, student_id, course_name):
        with patch('Flask_app.controller.session', db_session):
            res = controller_db.delete_course_from_student(student_id=student_id, course_name=course_name)

            assert not res
