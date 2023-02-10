from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from models import StudentModel, CourseModel, GroupModel, student_course
from engine_data import engine_data

engine = create_engine(engine_data)
session = Session(bind=engine)


class DataBase:
    @staticmethod
    def group_less_or_equal_students(count: int):
        groups = select(GroupModel).join(StudentModel).group_by(GroupModel.name) \
            .having(func.count(StudentModel.id) <= count)

        groups = session.scalars(groups)

        return groups

    @staticmethod
    def students_by_course_name(course_name):
        students = select(StudentModel) \
            .join(student_course) \
            .join(CourseModel) \
            .group_by(StudentModel.id) \
            .filter(CourseModel.name == course_name)

        students = session.scalars(students)

        return students

    @staticmethod
    def create_student(first_name: str, last_name: str, courses: list, group_name=None):
        if isinstance(first_name, str) and isinstance(last_name, str) \
                and len(courses) <= 3 and isinstance(group_name, str) or group_name is None:

            courses = select(CourseModel).filter(CourseModel.name.in_(courses))
            courses = session.scalars(courses).all()

            student = StudentModel(first_name=first_name,
                                   last_name=last_name,
                                   group_name=group_name,
                                   courses=courses)

            try:
                session.add(student)
                session.commit()
            except Exception as e:
                print(e)
                session.rollback()

    @staticmethod
    def delete_student(student_id: int):
        if isinstance(student_id, int):
            session.delete(session.scalar(select(StudentModel).filter(StudentModel.id == 21)))
            session.commit()

    @staticmethod
    def add_course_to_student(student_id: int, course_name: str):
        course = DataBase.__scalar_course_by_course_name(course_name)
        student = DataBase.__scalar_student_by_id(student_id)

        if course in student.courses:
            raise ValueError(f'Student (id {student.id}) already attend course "{course.name}"')

        student.courses.append(course)
        session.commit()

    @staticmethod
    def delete_course_from_student(student_id: int, course_name: str):
        course = DataBase.__scalar_course_by_course_name(course_name)
        student = DataBase.__scalar_student_by_id(student_id)

        if course not in student.courses:
            raise ValueError(f'Student (id {student.id}) doesnt attend course "{course.name}"')

        student.courses.remove(course)
        session.commit()

    @staticmethod
    def __scalar_course_by_course_name(course_name: str):
        course = select(CourseModel).filter(CourseModel.name == course_name)
        course = session.scalars(course).first()

        if not course:
            raise ValueError(f'Course "{course_name} doesnt exist"')

        return course

    @staticmethod
    def __scalar_student_by_id(student_id: int):
        student = select(StudentModel).filter(StudentModel.id == student_id)
        student = session.scalar(student)

        if not student:
            raise ValueError(f'Student with id {student_id} doesnt exist')

        return student
