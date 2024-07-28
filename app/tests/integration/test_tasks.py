from fastapi.testclient import TestClient
from app.main import app  
from app.schemas.task import TaskBase, TaskPatch

client = TestClient(app)

def create_task(title: str, description: str, completed: bool = False):
    new_task_data = {
        "title": title,
        "description": description,
        "completed": completed
    }
    response = client.post("/tasks/", json=new_task_data)
    assert response.status_code == 201
    response_data = response.json()
    return response_data["id"]

def test_read_tasks():
    task_ids = [
        create_task("Task 1", "Description 1"),
        create_task("Task 2", "Description 2"),
        create_task("Task 3", "Description 3", completed=True)
    ]
    
    response = client.get("/tasks/")
    assert response.status_code == 200
    response_data = response.json()

    assert len(response_data) == 3
    for task in response_data:
        assert "id" in task
        assert task["id"] in task_ids
        assert "title" in task
        assert "description" in task
        assert "completed" in task

def test_create_task():
    task_id = create_task("Test Task", "Description of the Test Task")
    assert task_id is not None

def test_read_task():
    task_id = create_task("Read Test Task", "Description of the Read Test Task")
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == task_id

def test_update_task_full():
    task_id = create_task("Full Update Task", "Description before update")
    update_data = TaskBase(
        title="Updated Task",
        description="Updated Description",
        completed=True
    )
    response = client.put(f"/tasks/{task_id}", json=update_data.model_dump())
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == update_data.title
    assert response_data["description"] == update_data.description
    assert response_data["completed"] == update_data.completed

def test_update_task_partial():
    task_id = create_task("Partial Update Task", "Description before partial update")
    partial_update_data = TaskPatch(
        completed=False
    )
    response = client.patch(f"/tasks/{task_id}", json=partial_update_data.model_dump(exclude_unset=True))
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["completed"] == partial_update_data.completed

def test_delete_task():
    task_id = create_task("Delete Task", "Task to be deleted")
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
