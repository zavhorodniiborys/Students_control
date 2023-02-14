from flask import jsonify, Blueprint, make_response
from flask_restful import Resource, Api, reqparse
from controller import controller_db

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
parser.add_argument('first_name', type=validate_name_length(1, 32), trim=True, location='form', help="Student's first name")
parser.add_argument('last_name', type=validate_name_length(1, 32), trim=True, location='form', help="Student's last name")
parser.add_argument('course', location='form', help="Student's course.", required=True,
                    choices=('Math', 'Biology', 'Physik', 'Chemistry', 'Literature',
                             'Psychology', 'Programming', 'Cybersecurity', 'Engineering', 'Law'))
parser.add_argument('group', type=validate_name_length(5, 5), trim=True, location='form', help="Student's group.")


class Courses(Resource):
    def put(self, course_name, student_id):
        remove_student = controller_db.delete_course_from_student(student_id=student_id, course_name=course_name)

        if remove_student:
            return 'Student successful removed', 200
        else:
            return 'Error while removing student', 400


class Groups(Resource):
    def get(self, student_count):
        groups = controller_db.group_less_or_equal_students(student_count)

        response = make_response(jsonify(groups))
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200

        return response


class Students(Resource):
    def get(self, course_name):
        students = controller_db.students_by_course_name(course_name)

        response = make_response(jsonify(students))
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200

        return response

    def post(self):
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        courses = [args['course']]
        group = args['group']

        new_student = controller_db.create_student(first_name=first_name, last_name=last_name,
                                                   courses=courses, group_name=group)

        if new_student:
            return 'Student successful added', 201
        else:
            return 'Error while adding student', 400

    def delete(self, student_id):
        controller_db.delete_student(student_id)

        return 'Deleted successful', 201

    def put(self, student_id):
        args = parser.parse_args()
        course = args['course']

        update_student = controller_db.add_course_to_student(student_id=student_id, course_name=course)

        if update_student:
            return 'Course successful added', 201
        else:
            return 'Error while adding course', 400


api.add_resource(Courses,
                 '/courses/<course_name>/remove_student/<int:student_id>')

api.add_resource(Groups,
                 '/groups/<int:student_count>')

api.add_resource(Students,
                 '/students/<course_name>',
                 '/students/add',
                 '/students/delete/<int:student_id>',
                 '/students/<int:student_id>/add_course')
