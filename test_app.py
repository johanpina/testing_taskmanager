from fastapi.testclient import TestClient
import pytest
from main import app, Task, task_manager

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks/", json={"title": "Test task", "description": "This is a test task", "status": "todo"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test task", "description": "This is a test task", "status": "todo"}

def test_read_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test task", "description": "This is a test task", "status": "todo"}

def test_update_task():
    response = client.put("/tasks/1", json={"title": "Updated task", "description": "This is an updated test task", "status": "doing"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Updated task", "description": "This is an updated test task", "status": "doing"}

def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

def test_read_all_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []

#########

def test_create_multiple_tasks():
    for i in range(5):
        response = client.post("/tasks/", json={"title": f"Test task {i+1}", "description": f"This is test task {i+1}", "status": "todo"})
        assert response.status_code == 200
        assert response.json() == {"id": i+1, "title": f"Test task {i+1}", "description": f"This is test task {i+1}", "status": "todo"}
"""
def test_read_all_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 5
"""

def test_read_nonexistent_task():
    response = client.get("/tasks/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_update_nonexistent_task():
    response = client.put("/tasks/100", json={"title": "Nonexistent task", "description": "This is a nonexistent task", "status": "doing"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_nonexistent_task():
    response = client.delete("/tasks/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}



def test_update_and_read_task():
    response = client.put("/tasks/1", json={"title": "Updated task", "description": "This is an updated test task", "status": "doing"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Updated task", "description": "This is an updated test task", "status": "doing"}

    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Updated task", "description": "This is an updated test task", "status": "doing"}

def test_delete_and_read_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

    response = client.get("/tasks/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_read_all_tasks_after_delete():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 4