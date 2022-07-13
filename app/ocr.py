import pathlib
import pytesseract
from PIL import Image

BASE_DIR =pathlib.Path(__file__).parent
IMG_DIR = BASE_DIR / "images"
img_path = IMG_DIR / "i2.jpg"

img = Image.open(img_path)

preds = pytesseract.image_to_string(img)

print(preds)