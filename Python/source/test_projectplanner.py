import pytest
from ProjectPlanner import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Project Resource Planner" in str(response.data)

def test_statistics(client):
    response = client.get('/statistics/')
    assert response.status_code == 200
    assert "No statistics available yet" in str(response.data)
