

def test_no_departments(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'There is no departments.' in response.data


def test_get_department_error(client):
    response = client.get('/department/1')
    assert response.status_code == 404


def test_add_department_get(client):
    response = client.get('/department/add')
    assert response.status_code == 200


def test_add_department_post(client):
    response = client.post('/department/add',
                           data={'name': 'test department'})
    assert response.status_code == 302


def test_get_department(client):
    response = client.get('/department/1')
    assert response.status_code == 200
    assert b'test department' in response.data


def test_get_departments(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'test department' in response.data


def test_update_department_get(client):
    response = client.get('/department/update/1')
    assert response.status_code == 200


def test_update_department_post(client):
    response = client.post('/department/update/1',
                           data={'name': 'new department'})
    assert response.status_code == 302
    response = client.get('/department/1')
    assert response.status_code == 200
    assert b'new department' in response.data


def test_update_department_error(client):
    response = client.post('/department/add',
                           data={'name': 'Testing department'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Testing department' in response.data
    response = client.post('/department/update/2',
                           data={'name': 'new department'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Department with this name already exists.' in response.data


def test_add_department_error(client):
    response = client.post('/department/add',
                           data={'name': 'Testing department'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Department already exists!' in response.data


def test_delete_department(client):
    response = client.get('/department/delete/1')
    assert response.status_code == 302
