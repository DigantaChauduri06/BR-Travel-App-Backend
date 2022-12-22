import os
from typing import Union
from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests;
from fastapi.middleware.cors import CORSMiddleware

import json
import wikipedia

from mangum import Mangum

# Initilize

origins = ["*"]


stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(title="BR Tours And Travels", openapi_prefix=openapi_prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/description/{place_name}")
def get_description(place_name):
    try :
        res = wikipedia.summary(place_name)
        return {"Success" : True, "data": res}
    except:
        return {"Success": False, "data": None}



@app.get("/images/{place_name}")
def get_images(place_name):
    url = f"https://unsplash.com/s/photos/{place_name}"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    res = []
    for img in soup.find_all("img"):
        res.append(img['src'])
    if not res:
        return {"Success": False, "photos": []}
    res.pop(0)
    print(len(res))
    return {"Success": True, "photos": res}


handler = Mangum(app)



