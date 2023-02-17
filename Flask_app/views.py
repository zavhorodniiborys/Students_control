from flask import jsonify, Blueprint, make_response
from flask_restful import Resource, Api, reqparse
from Flask_app.controller import controller_db

controller_blueprint = Blueprint('api_v1', __name__)
api = Api(controller_blueprint)


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
parser.add_argument('course', location='form', help="Student's course.",
                    choices=('Math', 'Biology', 'Physik', 'Chemistry', 'Literature',
                             'Psychology', 'Programming', 'Cybersecurity', 'Engineering', 'Law'))
parser.add_argument('group', type=validate_name_length(5, 5), trim=True, location='form', help="Student's group.")


class Courses(Resource):
    @staticmethod
    def put(course_name):
        args = parser.parse_args()
        student_id = args['student_id']

        remove_student = controller_db.delete_course_from_student(student_id=student_id, course_name=course_name)

        if remove_student:
            response = make_response('Student successful removed')
            response.status_code = 200
        else:
            response = make_response('Error while removing student')
            response.status_code = 400

        return response


class Groups(Resource):
    @staticmethod
    def get(student_count):
        groups = controller_db.group_less_or_equal_students(student_count)

        response = make_response(jsonify(groups))
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200

        return response


class Students(Resource):
    @staticmethod
    def get(course_name):
        students = controller_db.students_by_course_name(course_name)

        response = make_response(jsonify(students))
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200

        return response

    @staticmethod
    def post():
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        courses = [args['course']]
        group = args['group']

        new_student = controller_db.create_student(first_name=first_name, last_name=last_name,
                                                   courses=courses, group_name=group)

        if new_student:
            response = make_response('Student successful added')
            response.status_code = 201
        else:
            response = make_response('Error while adding student')
            response.status_code = 400

        return response

    @staticmethod
    def delete():
        args = parser.parse_args()
        student_id = args['student_id']

        if controller_db.delete_student(student_id):
            response = make_response('Deleted successful')
            response.status_code = 201
        else:
            response = make_response('No student with such id')
            response.status_code = 404

        return response

    @staticmethod
    def put():
        args = parser.parse_args()
        student_id = args['student_id']
        course = args['course']

        update_student = controller_db.add_course_to_student(student_id=student_id, course_name=course)

        if update_student:
            response = make_response('Course successful added')
            response.status_code = 201
        else:
            response = make_response('Error while adding course')
            response.status_code = 400

        return response


api.add_resource(Courses, '/courses/<course_name>/remove_student')
api.add_resource(Groups, '/groups/<int:student_count>')
api.add_resource(Students, '/students', '/students/<course_name>')
