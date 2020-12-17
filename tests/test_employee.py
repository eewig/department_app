import pytest


def test_no_employees(client):
    response = client.get('/employee')
    assert response.status_code == 200
    assert b'There is no employees.' in response.data


def test_get_employee_error(client):
    response = client.get('/employee/1')
    assert response.status_code == 404


def test_add_employee_get(client):
    response = client.get('/employee/add')
    assert response.status_code == 200


def test_add_employee_post(client):
    response = client.post('/employee/add',
                           data={'name': 'Tester', 'dob': '2000-10-10',
                                 'salary': 1000, 'department': 0})
    assert response.status_code == 302
    response = client.get('/employee/1')
    assert response.status_code == 200
    assert b'Tester' in response.data


@pytest.fixture(params=[('Jack', 'aa-10-10', 10, 0), ('Jack', '2000-10-10', 10, None)])
def test_add_employee_error(client, name, dob, salary, department):
    response = client.post('/employee/add',
                           data={'name': name, 'dob': dob,
                                 'salary': salary, 'department': department})

    assert response.status_code == 302
    assert b'Error! Check data you have entered.' in response.data


def test_update_employee_get(client):
    response = client.get('/employee/update/1')
    assert response.status_code == 200


def test_update_employee_post(client):
    response = client.post('/employee/update/1',
                           data={'name': 'Employee1', 'dob': '2000-10-10',
                                 'salary': 1000, 'department': 0})
    assert response.status_code == 302
    assert b'Error!' not in response.data
    response = client.get('/employee/1')
    assert response.status_code == 200
    assert b'Employee1' in response.data


@pytest.fixture(params=[('Jack', 'aa-10-10', 10, 0), ('Jack', '2000-10-10', 10, None)])
def test_update_employee_error(client):
    response = client.post('/employee/update/1',
                           data={'name': name, 'dob': dob,
                                 'salary': salary, 'department': department})
    assert response.status_code == 302
    assert b'Error! Check data you have entered.' in response.data


def test_get_employees(client):
    response = client.get('/employee')
    assert response.status_code == 200
    assert b'Employee' in response.data
    assert b'2000-10-10' in response.data


def test_delete_employee(client):
    response = client.get('/employee/delete/1')
    assert response.status_code == 302
