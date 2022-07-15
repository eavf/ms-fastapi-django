
import shutil
import time
import io
from fastapi.testclient import TestClient
from jinja2 import Template
from app.main import UPLOAD_DIR, app, BASE_DIR, UPLOAD_DIR, get_settings

from PIL import Image, ImageChops
import requests

ENDPOINT="https://fast-api-docker9-izaq2.ondigitalocean.app/"


def test_get_home():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']
    assert Template.debug_info


def test_invalid_file_upload_error():
    response = requests.post(ENDPOINT)
    assert response.status_code == 422
    assert "application/json" in response.headers['content-type']


def test_prediction_upload():
    img_saved_path =BASE_DIR / "images"
    settings = get_settings()
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = requests.post(ENDPOINT,
                               files={"file": open(path, 'rb')},
                               headers={"Authorization": f"JWT {settings.app_auth_token_prod}"})
        if img is not None:
            assert response.status_code == 200 or response.status_code == 504
            if response.status_code == 200:
                data = response.json()
                assert len(data.keys()) == 2
        else:
            assert response.status_code == 400
        print(response.headers)
        print(path.suffix)



def test_prediction_upload_missing_headers():
    img_saved_path =BASE_DIR / "images"
    settings = get_settings()
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = requests.post(ENDPOINT,
                               files={"file": open(path, 'rb')}
                               )
        assert response.status_code == 401 or response.status_code == 504 or response.status_code == 400