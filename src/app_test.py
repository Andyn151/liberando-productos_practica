from fastapi.testclient import TestClient
from src.application.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health": "ok"}

def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_bye():
    response = client.get("/bye")
    assert response.status_code == 200
    assert response.json() == {"msg": "Bye Bye"}
