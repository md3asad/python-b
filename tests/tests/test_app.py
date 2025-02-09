import pytest
from fastapi.testclient import TestClient
from app_b import app

client = TestClient(app)

def test_get_static_json():
    response = client.get("/api2")
    assert response.status_code == 200
    assert response.json() == {"message": "This is a static JSON", "status": "success"}

def test_get_host_name():
    response = client.get("/api3")
    assert response.status_code == 200
    json_data = response.json()
    assert "hostname" in json_data
    assert "datetime" in json_data
