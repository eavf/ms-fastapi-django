import json
import pathlib
import os
import io
import uuid
from functools import lru_cache
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    File,
    UploadFile,
    Request,
)
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates                          # nasztaviť templates
from pydantic import BaseSettings

# Zavedenie kontroly na debug alebo product environments
class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings ():
    return Settings()

# settings = Settings

settings = get_settings()
DEBUG = settings.debug


BASE_DIR = pathlib.Path(__file__).parent                                # nasztaviť templates
UPLOAD_DIR = BASE_DIR / "uploaded"

print ((BASE_DIR / "templates")  .exists())                             # nasztaviť templates

app = FastAPI()

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))      # nasztaviť templates

# REST API --> app to app --> ios to webapp - webapp.....

#@app.get("/")               # http GET -> JSON - s fastapi to vracia vždy vo forme JSON unless we change it
#def home_view():
    #return json.dumps({"hello": "world"})
    #return {}

#@app.get("/", response_class=HTMLResponse)        # http GET -> JSON - s fastapi to vracia vždy vo forme JSON unless we change it
#def home_view():
    #return "<h1>Hello World</h1>"

@app.get("/", response_class=HTMLResponse)        # http GET -> JSON - s fastapi to vracia vždy vo forme JSON unless we change it
def home_view(request: Request, settings:Settings = Depends(get_settings)):
    #print (request)
    print (settings.debug)
    return templates.TemplateResponse("home.html", {"request": request, "abc": 123, "ddd": settings.debug})

@app.post("/")              # http POST
def home_detail_view():
    return {"hello": "world"}

@app.post("/img-echo/", response_class=FileResponse)              # http POST
async def home_detail_view(file:UploadFile = File(...), settings:Settings = Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(detail="Invalid endpoint", status_code=400)
    bytes_str = io.BytesIO(await file.read())
    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    with open(str(dest), "wb") as out:
        out.write(bytes_str.read())
    return file