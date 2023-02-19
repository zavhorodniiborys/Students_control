from random import choice, randint
from string import ascii_uppercase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Flask_app.models import Base, StudentModel, GroupModel, CourseModel
from Flask_app.engine_data import engine_data


class CreateDBData:
    f_name = ('John', 'Alfred', 'Thomas', 'Mike', 'Steve', 'Eric', 'Kenny', 'Kyle', 'James', 'Jack',
              'Edward', 'Bob', 'Desmond', 'Charlie', 'Hugo', 'Ben', 'Benjamine', 'Jake', 'Bred', 'Boris')

    l_name = ('Lock', 'Black', 'Gray', 'Twain', 'Rodgers', 'Cartman', 'McCormic', 'Broflowsky', 'Cook', 'Shepard',
              'Callen', 'Big', 'Hume', 'Green', 'Raise', 'Churchill', 'Lienuss', 'Stone', 'Butter', 'Cool')

    courses = ('Math', 'Biology', 'Physik', 'Chemistry', 'Literature',
               'Psychology', 'Programming', 'Cybersecurity', 'Engineering', 'Law')

    @staticmethod
    def create_groups():
        groups = []

        for _ in range(20):
            chars = choice(ascii_uppercase) + choice(ascii_uppercase)
            nums = str(randint(0, 99)).zfill(2)

            group = '-'.join([chars, nums])

            groups.append(group)

        return groups

    @classmethod
    def create_students(cls):
        students = []

        for _ in range(200):
            name = (choice(cls.f_name), choice(cls.l_name))
            students.append(name)

        return students

    @classmethod
    def create_course_models(cls, session: Session) -> list:
        course_models = []

        for course in cls.courses:
            course_models.append(CourseModel(name=course))

        session.add_all(course_models)

        return course_models

    @classmethod
    def create_group_models(cls, session: Session) -> list:
        group_models = []
        groups = cls.create_groups()

        for group in groups:
            group_models.append(GroupModel(name=group))

        session.add_all(group_models)
        session.commit()

        return group_models

    @classmethod
    def create_student_model(cls, session: Session, students: list, courses: list, group_name=None):
        first_name, last_name = students.pop()

        courses_amount = randint(1, 3)
        students_courses = []

        for _ in range(courses_amount):
            course = choice(courses)
            while course in students_courses:
                course = choice(courses)

            students_courses.append(course)

        session.add(StudentModel(first_name=first_name,
                                 last_name=last_name,
                                 group_name=group_name,
                                 courses=students_courses
                                 ))

    @classmethod
    def set_up_db(cls):
        engine = create_engine(engine_data)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        session = Session(bind=engine)

        return session

    @classmethod
    def close_db(cls, session: Session):
        session.close()

    @classmethod
    def fill_db_data(cls):
        session = cls.set_up_db()

        groups = cls.create_group_models(session)
        courses = cls.create_course_models(session)
        students = cls.create_students()

        for group in groups:
            for _ in range(10, 30):
                if students:
                    cls.create_student_model(session=session, students=students,
                                             courses=courses, group_name=group.name)
                else:
                    break

        # if no more groups left
        for _ in range(len(students)):
            cls.create_student_model(session=session, students=students, courses=courses)


        # I also tried this code, but it fills only 100 elements to DB. I have no idea why
        # for _ in range(students):
        #     cls.create_student_model(session=session, students=students, courses=courses)


        session.commit()

        cls.close_db(session)


filler = CreateDBData()
filler.fill_db_data()
