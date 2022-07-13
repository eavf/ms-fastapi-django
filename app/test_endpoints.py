
import shutil
import time
import io
from fastapi.testclient import TestClient
from jinja2 import Template
from app.main import UPLOAD_DIR, app, BASE_DIR, UPLOAD_DIR

from PIL import Image, ImageChops

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


# Testovanie cez prípony súborov nie je spolahlivé
#valid_image_extensions = ['png', 'jpg', 'jpeg']

#def test_echo_upload():
#    img_saved_path =BASE_DIR / "images"
#
#    for path in img_saved_path.glob("*"):
#        response = client.post("/img-echo/", files={"file": open(path, 'rb')})      # requests.get("") python requests
#        fext = str(path.suffix).replace('.', '')
#        if fext in valid_image_extensions:
#            assert fext in response.headers['content-type']
#
#            assert response.status_code == 200
#        print(response.headers)
#        print(path.suffix)
#
#    time.sleep(3)
#    shutil.rmtree(UPLOAD_DIR)
#

#Test cez Image library
#Má problém, ak nie sú súbory jednoznačne zoraditeľné podľa poradia, neprejde test obrázka
#Je to pravdepodobne kvôli inému radeniu path a na serveri
#Má problém s JPG príponou!!!!!!!!!!
def test_echo_upload():
    img_saved_path =BASE_DIR / "images"
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = client.post("/img-echo/", files={"file": open(path, 'rb')})      # requests.get("") python requests
        if img is not None:
            assert response.status_code == 200
            r_stream = io.BytesIO(response.content)
            print("Response", response.url)
            echo_img = Image.open(r_stream)
            difference = ImageChops.difference(echo_img, img).getbbox()
            print(path, difference)
            assert difference is None
        else:
            assert response.status_code == 400
        print(response.headers)
        print(path.suffix)

    time.sleep(3)
    shutil.rmtree(UPLOAD_DIR)