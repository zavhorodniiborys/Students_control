from sqlalchemy import create_engine, select, func, delete, exc
from sqlalchemy.orm import Session
from .models import StudentModel, CourseModel, GroupModel, student_course
from .engine_data import engine_data

engine = create_engine(engine_data)
session = Session(engine)


class ControllerDataBase:
    @staticmethod
    def get_groups_with_less_or_equal_students(count: int):
        query_groups = select(GroupModel.name).outerjoin(StudentModel).group_by(GroupModel.name) \
            .having(func.count(StudentModel.id) <= count)

        fetched_groups = session.execute(query_groups).all()

        groups = {'groups': [{'name': name[0]} for name in fetched_groups]}

        return groups

    @staticmethod
    def students_by_course_id(course_id):
        query_students = select(StudentModel.id) \
            .join(student_course) \
            .join(CourseModel) \
            .group_by(StudentModel.id) \
            .filter(CourseModel.id == course_id)

        fetched_students = session.execute(query_students).all()

        students = {'students': [{'id': student.id} for student in fetched_students]}

        return students

    @staticmethod
    def create_student(first_name: str, last_name: str, courses: list, group_name=None):
        if isinstance(first_name, str) and isinstance(last_name, str) \
                and len(courses) <= 3 and isinstance(group_name, str) or group_name is None:

            courses = select(CourseModel).filter(CourseModel.id.in_(courses))
            courses = session.scalars(courses).all()

            student = StudentModel(first_name=first_name,
                                   last_name=last_name,
                                   group_name=group_name,
                                   courses=courses)

            try:
                session.add(student)
                session.commit()

                return {'student': {'id': student.id}}

            except exc.SQLAlchemyError:
                session.rollback()
                return False

    @staticmethod
    def delete_student(student_id: int):
        try:
            session.execute(delete(StudentModel).where(StudentModel.id == student_id))
            session.commit()
            return True

        except exc.SQLAlchemyError:
            return False

    @staticmethod
    def add_course_to_student(student_id: int, course_id: int):
        add_course_query = student_course.insert().values(student_id=student_id, course_id=course_id)
        try:
            session.execute(add_course_query)
            session.commit()

        except exc.SQLAlchemyError as error:
            session.rollback()
            raise error

    @staticmethod
    def delete_course_from_student(student_id: int, course_id: int):
        delete_course_query = student_course.delete().filter(student_course.c.student_id == student_id,
                                                             student_course.c.course_id == course_id)
        try:
            session.execute(delete_course_query)
            session.commit()
            return True

        except exc.SQLAlchemyError:
            return False


controller_db = ControllerDataBase()
