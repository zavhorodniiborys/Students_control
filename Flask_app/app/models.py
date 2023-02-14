from typing import List, Optional
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


student_course = Table('student_course', Base.metadata,
                       Column('student_id', ForeignKey('student.id'), primary_key=True),
                       Column('course_name', ForeignKey('course.name'), primary_key=True))


class CourseModel(Base):
    __tablename__ = 'course'

    name: Mapped[str] = mapped_column(String(32), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String(1024))

    students: Mapped[List['StudentModel']] = relationship(secondary=student_course, back_populates='courses')


class StudentModel(Base):
    __tablename__ = 'student'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))

    group_name: Mapped[Optional[str]] = mapped_column(ForeignKey('group.name'))

    courses: Mapped[List[CourseModel]] = relationship(secondary=student_course, back_populates='students')


class GroupModel(Base):
    __tablename__ = 'group'

    name: Mapped[str] = mapped_column(String(5), primary_key=True)
