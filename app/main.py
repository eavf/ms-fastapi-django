import json
import pathlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates                          # nasztaviť templates

BASE_DIR = pathlib.Path(__file__).parent                                # nasztaviť templates
#print ((BASE_DIR / "templates")  .exists())                             # nasztaviť templates

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
def home_view(request: Request):
    #print (request)

    return templates.TemplateResponse("home.html", {"request": request, "abc": 123})

@app.post("/")              # http POST
def home_detail_view():
    return {"hello": "world"}
