def create_task(fast_api_test_client, name="Test Task", parent_id=None):
    response = fast_api_test_client.post("/tasks", json={"name": name, "parent_id": parent_id})
    return response.json()


def test_filter_by_status(fast_api_test_client):
    create_task(fast_api_test_client, name="CompletedTask")
    fast_api_test_client.post("/tasks/1/fork")  # Fork to get a child

    # Simulate task update to completed
    response = fast_api_test_client.get("/tasks", params={"status": "running"})
    assert response.status_code == 200
    data = response.json()
    assert all(task["status"] == "running" for task in data["items"])


def test_pagination(fast_api_test_client):
    # Ensure we have multiple tasks
    for i in range(5):
        create_task(fast_api_test_client, name=f"Task{i}")

    response = fast_api_test_client.get("/tasks", params={"limit": 2, "offset": 0})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 2
    assert "total" in data


def test_fork_task(fast_api_test_client):
    parent = create_task(fast_api_test_client, name="Parent")
    response = fast_api_test_client.post(f"/tasks/{parent['id']}/fork")
    assert response.status_code == 201
    child = response.json()
    assert child["parent_id"] == parent["id"]


def test_delete_task(fast_api_test_client):
    task = create_task(fast_api_test_client, name="ToDelete")

    # Delete the task
    response = fast_api_test_client.delete(f"/tasks/{task['id']}")
    assert response.status_code == 200

    # Try to get the task again
    response = fast_api_test_client.get(f"/tasks/{task['id']}")
    item = response.json()
    task_status = item.get("status")
    assert task_status == "killed"


def test_invalid_task_creation(fast_api_test_client):
    response = fast_api_test_client.post("/tasks", json={})
    assert response.status_code == 422


def test_fork_nonexistent_task(fast_api_test_client):
    task_id = 9999  # Assuming this ID does not exist
    response = fast_api_test_client.post(f"/tasks/{task_id}/fork")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with ID {task_id} not found"


def test_filter_by_nonexistent_status(fast_api_test_client):
    response = fast_api_test_client.get("/tasks", params={"status": "nonsense"})
    assert response.status_code == 422


def test_sorting(fast_api_test_client):
    create_task(fast_api_test_client, name="Zebra")
    create_task(fast_api_test_client, name="Alpha")

    response = fast_api_test_client.get("/tasks", params={"sort_by": "name", "order": "asc"})
    assert response.status_code == 200

    # Filter only the relevant ones
    data = response.json()["items"]
    names = [task["name"] for task in data if task["name"] in ["Zebra", "Alpha"]]

    assert names == sorted(names)
