import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Flask_app.app.controller import controller_db
from Flask_app.app.models import Base, StudentModel, CourseModel, GroupModel

# зробив це для наочності, щоб показати, що для тестів я створив окрему базу даних
engine = create_engine('postgresql+psycopg2://boris:cool_pass@127.0.0.1:5432/test_db')


@pytest.fixture(scope='class')
def db_session():
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope='class')
def valid_student():
    student = StudentModel(first_name='John',
                           last_name='Doe',
                           group_name='group_name',
                           courses='students_courses'
                           )


class TestControllerDataBase:
    def test_group_less_or_equal_students(self):
        pass

    def test_students_by_course_name(self):
        pass

    def test_create_student(self):
        pass

    def test_delete_student(self):
        pass

    def test_add_course_to_student(self):
        pass

    def test_delete_course_from_student(self):
        pass
