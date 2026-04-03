from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    # Змінюємо очікуваний рядок тут:
    assert response.json() == {"status": "ok", "message": "App is running"}