
from fastapi.testclient import TestClient
from jinja2 import Template
from app.main import app

client = TestClient(app)            # r = requests


def test_get_home():
    response = client.get("/")      # requests.get("") python requests
    assert response.status_code == 200
    #assert response.headers['content-type'] == "text/html"
    assert "text/html" in response.headers['content-type']
    #assert response.
    assert Template.debug_info


def test_post_home():
    response = client.post("/")      # requests.get("") python requests
    assert response.status_code == 200
    #assert response.headers['content-type'] == "text/html"
    assert "application/json" in response.headers['content-type']
    assert response.json() == {"hello": "world"}