from flask import jsonify, Blueprint, make_response
from flask_restful import Resource, Api, reqparse
from Flask_app.controller import controller_db

controller_views_api = Blueprint('api_v1', __name__)
api = Api(controller_views_api)


def validate_name_length(min_len, max_len):
    def validate(name: str):
        if not isinstance(name, str):
            raise ValueError("Attribute 'name' bust be a string.")

        if len(name.strip()) < min_len:
            raise ValueError("Attribute 'name' can not be empty.")
        elif len(name.strip()) > max_len:
            raise ValueError(f"Attribute 'name' too long. Max length is {max_len} characters.")

        return name

    return validate


parser = reqparse.RequestParser()
parser.add_argument('student_id', type=int, trim=True, location='form', help="Student`s id")
parser.add_argument('first_name', type=validate_name_length(1, 32), trim=True, location='form',
                    help="Student's first name")
parser.add_argument('last_name', type=validate_name_length(1, 32), trim=True, location='form',
                    help="Student's last name")
parser.add_argument('course_id', type=int, location='form', help="Student's course.")
parser.add_argument('group', type=validate_name_length(5, 5), trim=True, location='form', help="Student's group.")


class Base:
    @staticmethod
    def create_response(status_code, message, content_type=None):
        if content_type == 'application/json':
            response = make_response(jsonify(message))
            response.headers['Content-Type'] = 'application/json'

        else:
            response = make_response(message)

        response.status_code = status_code

        return response


class Courses(Resource, Base):
    @classmethod
    def delete(cls):
        args = parser.parse_args()
        student_id = args['student_id']
        course_id = args['course_id']

        remove_student = controller_db.delete_course_from_student(student_id=student_id, course_id=course_id)

        if remove_student:
            response = cls.create_response(200, 'Student successful removed')

        else:
            response = cls.create_response(400, 'Error while removing student')

        return response


class Groups(Resource, Base):
    @classmethod
    def get(cls, student_count):
        groups = controller_db.groups_with_less_or_equal_students(student_count)

        response = cls.create_response(200, groups, 'application/json')

        return response


class Students(Resource, Base):
    @classmethod
    def get(cls, course_id):
        students = controller_db.students_by_course_id(course_id)

        response = cls.create_response(200, students, 'application/json')

        return response

    @classmethod
    def post(cls):
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        courses = [args['course']]
        group = args['group']

        new_student = controller_db.create_student(first_name=first_name, last_name=last_name,
                                                   courses=courses, group_name=group)

        if new_student:
            response = cls.create_response(201, 'Student successful added')
        else:
            response = cls.create_response(400, 'Error while adding student')

        return response

    @classmethod
    def delete(cls):
        args = parser.parse_args()
        student_id = args['student_id']

        if controller_db.delete_student(student_id):
            response = cls.create_response(201, 'Deleted successful')
        else:
            response = cls.create_response(404, 'No student with such id')

        return response

    @classmethod
    def put(cls):
        args = parser.parse_args()
        student_id = args['student_id']
        course = args['course_id']

        update_student = controller_db.add_course_to_student(student_id=student_id, course_id=course)

        if update_student:
            response = cls.create_response(201, 'Course successful added')
        else:
            response = cls.create_response(400, 'Error while adding course')

        return response


api.add_resource(Courses, '/courses')
api.add_resource(Groups, '/groups/<int:student_count>')
api.add_resource(Students, '/students', '/students/<int:course_id>')
