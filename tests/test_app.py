import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Task Board" in response.data


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_task_list_starts_empty(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_task(client):
    response = client.post("/api/tasks", json={"title": "Write Jenkinsfile"})
    assert response.status_code == 201
    body = response.get_json()
    assert body["id"] == 1
    assert body["title"] == "Write Jenkinsfile"
    assert body["done"] is False


def test_add_task_requires_title(client):
    response = client.post("/api/tasks", json={"title": "   "})
    assert response.status_code == 400
    assert response.get_json()["error"] == "title is required"


def test_get_task_by_id(client):
    client.post("/api/tasks", json={"title": "Run pytest"})
    response = client.get("/api/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Run pytest"


def test_complete_task(client):
    client.post("/api/tasks", json={"title": "Publish JUnit"})
    response = client.post("/api/tasks/1/complete")
    assert response.status_code == 200
    assert response.get_json()["done"] is True


def test_delete_task(client):
    client.post("/api/tasks", json={"title": "Remove me"})
    response = client.delete("/api/tasks/1")
    assert response.status_code == 200
    assert response.get_json() == {"deleted": 1}
    assert client.get("/api/tasks").get_json() == []


def test_stats_count_done_and_pending(client):
    client.post("/api/tasks", json={"title": "One"})
    client.post("/api/tasks", json={"title": "Two"})
    client.post("/api/tasks/1/complete")
    response = client.get("/api/stats")
    assert response.status_code == 200
    assert response.get_json() == {"total": 2, "done": 1, "pending": 1}


def test_missing_task_returns_404(client):
    response = client.get("/api/tasks/99")
    assert response.status_code == 404
    assert response.get_json()["error"] == "not found"
