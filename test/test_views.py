# import pytest
# from unittest.mock import patch
# from flask import jsonify, test_client
# from Flask_app.app import app
#
#
# @pytest.fixture()
# def client():
#     return app.test_client()
#
#
# class TestGroups:
#     test_example = {
#         'groups': [
#             {'name': 'AB-12'},
#             {'name': 'QW-23'}
#         ]
#     }
#
#     @patch('Flask_app.views.controller_db.group_less_or_equal_students', test_example)
#     def test_get(self, client):
#         responce = client.get('/groups/5')
#
#         assert responce.status_code == 200
#         assert responce.headers['Content=Type'] == 'application/json'
#         assert responce.data == jsonify(self.test_example)
#
#
# class TestCourses:
#     @pytest.mark.parametrize('query_res, status_code, data', (
#             (True, 200, 'Student successful removed'),
#             (False, 400, 'Error while removing student')
#     ))
#     def test_put(self, client, query_res, status_code, data):
#         with patch('Flask_app.views.controller_db.delete_course_from_student', query_res):
#             responce = client.put('/courses/<course_name>/remove_student/student')
#
#             assert responce.status_code == status_code
#             assert responce.data == data
#
#
# class TestStudent:
#     test_get_example = {
#         'students': [
#             {'id': 1},
#             {'id': 2}
#         ]
#     }
#
#     @patch('Flask_app.views.controller_db.students_by_course_name', test_get_example)
#     def test_get(self, client):
#         responce = client.get('/students/<course_name>')
#
#         assert responce.status_code == 200
#         assert responce.headers['Content=Type'] == 'application/json'
#         assert responce.data == jsonify(self.test_example)
#
#     @pytest.mark.parametrize('patcher_create_student, status_code, data', (
#             (True, 201, 'Student successful added'),
#             (False, 400, 'Error while adding student')
#     ))
#     def test_post(self, client, patcher_create_student, status_code, data):
#         with patch('Flask_app.views.controller_db.create_student', patcher_create_student):
#             responce = client.post('/students/', data={'first_name': None,
#                                                        'last_name': None,
#                                                        'courses ': None,
#                                                        'group': None})
#
#             assert responce.status_code == status_code
#             assert responce.headers['Content=Type'] == 'application/json'
#             assert responce.data == data
#
#     def test_delete(self, client):
#         with patch('Flask_app.views.controller_db.delete_student', None):
#             responce = client.delete('/students/', data={'student_id': None})
#
#             assert responce.status_code == 201
#             assert responce.data == 'Deleted successful'
#
#     @pytest.mark.parametrize('query_res, status_code, data', (
#             (True, 201, 'Course successful added'),
#             (False, 400, 'Error while adding course')
#     ))
#     def test_put(self, client, query_res, status_code, data):
#         with patch('Flask_app.views.controller_db.add_course_to_student', query_res):
#             responce = client.put('/students/', data={'course': None})
#
#             assert responce.status_code == status_code
#             assert responce.data == data
