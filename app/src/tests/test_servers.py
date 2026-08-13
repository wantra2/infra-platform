def server_payload():
    return {
        "hostname": "web-01",
        "environment": "production",
        "region": "eu-west-1",
        "status": "running",
        "cpu": 4,
        "memory_gb": 16,
        "owner": "platform",
    }


def test_create_server(client):
    response = client.post(
        "/api/v1/servers",
        json=server_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["hostname"] == "web-01"
    assert data["environment"] == "production"
    assert data["cpu"] == 4
    assert data["memory_gb"] == 16
    assert data["owner"] == "platform"
    assert data["status"] == "running"
    assert "id" in data
    assert "created_at" in data


def test_get_server(client):
    create_response = client.post(
        "/api/v1/servers",
        json=server_payload(),
    )

    server_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/servers/{server_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == server_id
    assert data["hostname"] == "web-01"


def test_get_nonexistent_server(client):
    response = client.get("/api/v1/servers/999999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Server not found",
    }


def test_list_servers(client):
    response = client.get("/api/v1/servers")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_update_server(client):
    create_response = client.post(
        "/api/v1/servers",
        json=server_payload(),
    )

    server_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/servers/{server_id}",
        json={
            "status": "stopped",
            "cpu": 8,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "stopped"
    assert data["cpu"] == 8

    # Verify persistence
    response = client.get(
        f"/api/v1/servers/{server_id}"
    )

    data = response.json()

    assert data["status"] == "stopped"
    assert data["cpu"] == 8


def test_delete_server(client):
    create_response = client.post(
        "/api/v1/servers",
        json=server_payload(),
    )

    server_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/servers/{server_id}"
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/servers/{server_id}"
    )

    assert response.status_code == 404


def test_delete_nonexistent_server(client):
    response = client.delete(
        "/api/v1/servers/999999"
    )

    assert response.status_code == 404

def test_duplicate_hostname(client):
    payload = server_payload()

    first = client.post(
        "/api/v1/servers",
        json=payload,
    )

    assert first.status_code == 201

    second = client.post(
        "/api/v1/servers",
        json=payload,
    )

    assert second.status_code == 409

    assert second.json() == {
        "detail": "Hostname already exists",
    }

def test_invalid_server_payload(client):
    payload = server_payload()

    payload["cpu"] = "not-a-number"

    response = client.post(
        "/api/v1/servers",
        json=payload,
    )

    assert response.status_code == 422

def test_partial_update(client):
    create_response = client.post(
        "/api/v1/servers",
        json=server_payload(),
    )

    server_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/servers/{server_id}",
        json={
            "memory_gb": 32,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["memory_gb"] == 32

    # Existing fields must remain unchanged
    assert data["hostname"] == "web-01"
    assert data["cpu"] == 4
    assert data["status"] == "running"