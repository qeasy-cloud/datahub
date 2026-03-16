from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "QEasy DataHub API"
    assert data["health_url"] == "/api/v1/health"


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_project_endpoint() -> None:
    response = client.get("/api/v1/project")
    assert response.status_code == 200
    data = response.json()
    assert data["company"] == "广东轻亿云软件科技有限公司"
