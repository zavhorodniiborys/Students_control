from sqlalchemy import create_engine, text, MetaData, select
from sqlalchemy.orm import Session
from models import StudentModel, CourseModel, GroupModel, student_course
from populate_db import CreateDBData
from engine_data import engine_data

engine = create_engine(engine_data, echo=True)


# StudentModel.metadata.drop_all(engine)
StudentModel.metadata.create_all(engine)

with Session(engine) as session:
    db_filler = CreateDBData

    students = db_filler.create_students()
    print(students)

    # person = select(StudentModel).where(StudentModel.id == 2)
    # res = session.execute(person)
    # for user in res.scalars():
    #     print(user.first_name, user.last_name, user.group_name, user.courses, 'HELLO')
        # user.courses.name.add= 'Math'
        # print(user.courses[0].name)

    # st_by_course = select(StudentModel).where(StudentModel.courses)
    # st_by_course = session.execute(st_by_course)
    # for st in st_by_course.scalars():
    #     print('\n\n', st.first_name, st.last_name, '\n')

    def get_student_by_course(course):
        query = select(StudentModel).where(StudentModel.courses.any(name='Math'))
        students = session.execute(query)
        for student in students.scalars():
            print('\nHELLO THERE\n', student.first_name, student.last_name)


    etalon_st = StudentModel(first_name='Etalon', last_name='Student', group_name='WP-92',
                             courses=[CourseModel(name='Test', description='info')])
    session.add(etalon_st)



    # course = select(CourseModel).where(CourseModel.name == 'Math')
    # res = session.execute(course)
    # res = res.scalar_one()
    #
    # print('\n\n', res.name, '\n\n')
    #
    # soyer = StudentModel(first_name='James', last_name='Ford')
    # soyer.courses.append(res)
    # session.add_all([soyer])



    # for group in db_filler.create_group():
    #     session.add_all([GroupModel(name=group)])



    # for student in students:
    #
    #     st = StudentModel(first_name=student[0], last_name=student[1])
    #     session.add_all([st])





    # courses = db_filler.courses
    # for course in courses:
    #
    #     session.add_all([CourseModel(name=course, description='test')])

    session.commit()
