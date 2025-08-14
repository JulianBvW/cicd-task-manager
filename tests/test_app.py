import pytest
from src.app import app, tasks


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        tasks.clear()  # Clear tasks before each test
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello CI/CD' in response.data


def test_get_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_task(client):
    response = client.post('/tasks', json={'title': 'Buy vegan milk'})
    assert response.status_code == 201
    task = response.get_json()
    assert task['id'] == 1
    assert task['title'] == 'Buy vegan milk'
    assert task['done'] is False


def test_add_task_missing_title(client):
    response = client.post('/tasks', json={})
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_get_tasks_after_adding(client):
    response = client.post('/tasks', json={'title': 'Buy vegan milk'})
    assert response.status_code == 201
    task = response.get_json()
    assert task['title'] == 'Buy vegan milk'
    assert task['done'] is False

    response = client.get('/tasks')
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 1
    assert tasks[0] == task


def test_delete_task(client):
    # First add a task
    post_response = client.post('/tasks', json={'title': 'Buy vegan milk'})
    task_id = post_response.get_json()['id']

    # Delete the task
    delete_response = client.delete(f'/tasks/{task_id}')
    assert delete_response.status_code == 204

    # Verify the task is deleted
    get_response = client.get('/tasks')
    assert get_response.status_code == 200
    tasks = get_response.get_json()
    assert len(tasks) == 0


def test_delete_task_not_found(client):
    response = client.delete('/tasks/999')
    assert response.status_code == 404
    assert 'error' in response.get_json()
