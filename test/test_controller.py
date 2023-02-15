import pytest
from unittest.mock import patch
from sqlalchemy import create_engine, select
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


@pytest.fixture(scope='class')
def valid_students():
    student = StudentModel(first_name='John',
                           last_name='Doe',
                           group_name='group_name',
                           courses='students_courses')

    return student


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
              GroupModel(name='CB-30'))

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

    session.add(GroupModel(name='O1-45'))
    print(session.execute(select(CourseModel)).all())
    session.add_all([*groups, *courses, *students])
    session.commit()


class TestControllerDataBase:
    @pytest.mark.parametrize('count, expected_res', [
        (3, ['Math', 'Biology', 'Law', 'OO-00']),
        (0, ['OO-00'])
    ])
    def test_group_less_or_equal_students(self, db_session, count, expected_res):
        with patch('Flask_app.controller.session', db_session):
            # print(db_session.execute(select(CourseModel)).all())
            groups = controller_db.group_less_or_equal_students(count)['groups']
            names = [group['name'] for group in groups]

            assert names == expected_res
    #
    # def test_students_by_course_name(self):
    #     students = controller_db.students_by_course_name('Biology')['students']
    #     students_id = [student['id'] for student in students]
    #
    #     expected_res = [4, 5, 6]
    #
    #     assert students_id == expected_res
    #
    # @pytest.mark.parametrize('course_name', [['Math'], None])
    # def test_create_student(self, course_name):
    #     res = controller_db.create_student(first_name='Test',
    #                                        last_name='Example',
    #                                        courses=course_name,
    #                                        group_name='CB-30')
    #
    #     assert res == 1
    #
    # def test_create_student_error(self):
    #     pass
    #
    # def test_delete_student(self):
    #     pass
    #
    # @pytest.mark.xfail()
    # def test_delete_student_error(self):
    #     pass
    #
    # def test_add_course_to_student(self, student_id=1, course_name='Law'):
    #     res = controller_db.add_course_to_student(student_id=student_id, course_name=course_name)
    #
    #     assert res == True
    #
    # def test_add_course_to_student_error(self, student_id=1, course_name='Math'):
    #     with pytest.raises(ValueError,
    #                        match=f'Student (id {student_id}) already attend course "{course_name}"'):
    #         controller_db.add_course_to_student(student_id=student_id, course_name=course_name)
    #
    # def test_delete_course_from_student(self):
    #     pass
    #
    # def test_delete_course_from_student_error(self, student_id=1, course_name='Biology'):
    #     with pytest.raises(ValueError,
    #                        match=f'Student (id {student_id}) doesnt attend course "{course_name}"'):
    #         controller_db.delete_course_from_student(student_id=student_id, course_name=course_name)

if __name__ == '__main__':
    pytest.main()
