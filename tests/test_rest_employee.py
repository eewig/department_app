import os
import pytest


def test_get_no_employees(client):
    response = client.get('/api/employee')
    assert response.status_code == 204
    assert response.data == b''


def test_get_employee_error(client):
    response = client.get('/api/employee/1')
    assert response.status_code == 404


def test_post_employee_error(client):
    response = client.post('/api/employee', json={})
    assert response.status_code == 400


def test_post_employee(client):
    response = client.post('/api/department', json={'name': 'Dev'})
    assert response.status_code == 201
    response = client.post('/api/employee', json={'name': 'John',
        'dob': '2000-10-10', 'salary': 1000, 'department_id': 1})
    assert response.status_code == 201
    assert response.get_json() == {'name': 'John', 'dob': '2000-10-10',
        'salary': 1000, 'department_id': 1}


def test_get_employees(client):
    response = client.post('/api/employee', json={'name': 'Friedrich',
        'dob': '1999-09-09', 'salary': 1000})
    assert response.status_code == 201
    response = client.get('/api/employee')
    assert response.status_code == 200
    assert response.get_json() == [{'id':1, 'name': 'John',
        'dob': '2000-10-10', 'salary': 1000, 'department_id': 1},
        {'id': 2, 'name': 'Friedrich', 'dob': '1999-09-09',
        'salary': 1000, 'department_id': None}]


def test_get_employee(client):
    response = client.get('/api/employee/1')
    assert response.status_code == 200
    assert response.get_json() == {'id':1, 'name': 'John',
        'dob': '2000-10-10', 'salary': 1000, 'department_id': 1}


def test_put_employee_partial(client):
    response = client.put('/api/employee/1',
        json={'name': 'Jack', 'salary': 2000})
    assert response.status_code == 204


def test_put_employee_full(client):
    response = client.put('/api/employee/1',
        json={'name': 'John', 'dob': '2000-10-10', 'salary': 1000,
        'department_id': 1})
    assert response.status_code == 204


def test_employee_by_department_id(client):
    response = client.get('/api/employee', query_string={'department_id': 1})
    assert response.status_code == 200
    assert response.get_json() == [{'id':1, 'name': 'John',
        'dob': '2000-10-10', 'salary': 1000, 'department_id': 1}]


@pytest.mark.skipif(os.getenv('GITLAB_CI') is None,
    reason='SQLite doesnt have date field type')
def test_dob_filter(client):
    response = client.get('/api/employee',
        query_string={'dob':'2000-10-10'})
    assert response.status_code == 200
    assert response.get_json() == [{'id':1, 'name': 'John',
        'dob': '2000-10-10', 'salary': 1000, 'department_id': 1}]


def test_dob_filter_range(client):
    response = client.get('/api/employee',
        query_string={'dob':'1999-09-01', 'dob_end': '2001-10-10'})
    assert response.status_code == 200
    assert response.get_json() == [{'id':1, 'name': 'John',
        'dob': '2000-10-10', 'salary': 1000, 'department_id': 1},
        {'id': 2, 'name': 'Friedrich', 'dob': '1999-09-09',
        'salary': 1000, 'department_id': None}]


def test_dob_filter_error(client):
    response = client.get('/api/employee',
        query_string={'dob': '10-10-2000'})
    assert response.status_code == 400
    assert response.get_json() == {'message':
        'Wrong time format! (yyyy-mm-dd)'}


@pytest.fixture(scope="module", params=[('10-aaa-2000', '1999-01-01'),
    ('10-10-2010', '1990-10-10'), ('1111-13-13', '2000-01-01')])
def test_dob_filter_range_error(client, dob, dob_end):
    response = client.get('/api/employee',
        query_string={'dob': dob, 'dob_end': dob_end})
    assert response.status_code == 400
    assert response.get_json() == {'message':
        'Wrong time format! (yyyy-mm-dd)'}

def test_delete_employee(client):
    response = client.delete('/api/employee/2')
    assert response.status_code == 204
