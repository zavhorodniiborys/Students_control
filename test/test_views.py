import pytest
from unittest.mock import patch
from flask import jsonify
from Flask_app.app import app


@pytest.fixture(scope='module')
def client():
    return app.test_client()


class TestGroups:
    test_example = {
        'groups': [
            {'name': 'AB-12'},
            {'name': 'QW-23'}
        ]
    }

    @patch('Flask_app.views.controller_db.groups_with_less_or_equal_students', return_value=test_example)
    def test_get(self, patcher, client):
        with client:
            response = client.get('http://127.0.0.1:5000/groups/5')

            assert response.status_code == 200
            assert response.headers['Content-Type'] == 'application/json'
            assert response.data == jsonify(self.test_example).data


class TestCourses:
    @pytest.mark.parametrize('query_res, status_code, data', (
            (True, 200, b'Student successful removed'),
            (False, 400, b'Error while removing student')
    ))
    def test_put(self, client, query_res, status_code, data):
        with patch('Flask_app.views.controller_db.delete_course_from_student', return_value=query_res):
            with client:
                response = client.put('http://127.0.0.1:5000/courses/course_name/remove_student',
                                      data={'student_id': 1})

                assert response.status_code == status_code
                assert response.data == data


class TestStudent:
    test_example = {
        'students': [
            {'id': 1},
            {'id': 2}
        ]
    }

    @patch('Flask_app.views.controller_db.students_by_course_name', return_value=test_example)
    def test_get(self, patcher, client):
        with client:
            response = client.get('http://127.0.0.1:5000/students/course_name')

            assert response.status_code == 200
            assert response.headers['Content-Type'] == 'application/json'
            assert response.data == jsonify(self.test_example).data

    @pytest.mark.parametrize('query_res, status_code, data', (
            (True, 201, b'Student successful added'),
            (False, 400, b'Error while adding student')
    ))
    def test_post(self, client, query_res, status_code, data):
        with patch('Flask_app.views.controller_db.create_student', return_value=query_res):
            response = client.post('http://127.0.0.1:5000/students', data={'first_name': None,
                                                                           'last_name': None,
                                                                           'courses ': None,
                                                                           'group': None})
            assert response.status_code == status_code
            assert response.data == data

    @pytest.mark.parametrize('query_res, status_code, data', (
            (True, 201, b'Deleted successful'),
            (False, 404, b'No student with such id')
    ))
    def test_delete(self, client, query_res, status_code, data):
        with patch('Flask_app.views.controller_db.delete_student', return_value=query_res):
            response = client.delete('http://127.0.0.1:5000/students', data={'student_id': None})

            assert response.status_code == status_code
            assert response.data == data

    @pytest.mark.parametrize('query_res, status_code, data', (
            (True, 201, b'Course successful added'),
            (False, 400, b'Error while adding course')
    ))
    def test_put(self, client, query_res, status_code, data):
        with patch('Flask_app.views.controller_db.add_course_to_student', return_value=query_res):
            response = client.put('/students', data={'course': None, 'student_id': None})

            assert response.status_code == status_code
            assert response.data == data
