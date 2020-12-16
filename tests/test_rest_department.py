def test_api_department_error(client):
    response = client.get('/api/department')
    rv = client.post('/api/department')

    assert response.status_code == 204
    assert response.data == b''
    assert rv.status_code == 400
    assert rv.get_json() == {'message': 'Data is not valid.'}


def test_department_post(client):
    response = client.post('/api/department',
                           json={'name': 'test_department'})
    assert response.status_code == 201
    assert response.get_json() == {'name': 'test_department'}


def test_api_department_list(client):
    response = client.get('/api/department')
    assert response.get_json() == [
                                 {'employees': [],
                                  'id': 1,
                                  'name': 'test_department'}]
    assert response.status_code == 200


def test_api_department_error(client):
    response = client.get('/api/department/2')
    assert response.status_code == 404


def test_api_department_put(client):
    response = client.put('/api/department/1', json={'name': 'new_department'})
    assert response.status_code == 204


def test_api_department_get(client):
    response = client.get('/api/department/1')
    assert response.status_code == 200
    assert response.get_json() == {"employees": [], "id": 1,
                                   "name": "new_department"}


def test_get_departments_avg_salary(client):
    response = client.post('/api/employee',
                           json={'name': 'Jack', 'dob': '2000-01-01',
                                 'salary': 500, 'department_id': 1})
    response = client.post('/api/employee',
                           json={'name': 'John', 'dob': '2000-01-01',
                                 'salary': 1500, 'department_id': 1})
    response = client.get('/api/department',
                          query_string={'avg': 1})
    assert response.status_code == 200
    assert response.get_json() == [{'id': 1, 'name': 'new_department',
                                    'average-salary': 1000.0}]


def test_api_department_delete(client):
    response = client.delete('/api/department/1')
    assert response.status_code == 204
