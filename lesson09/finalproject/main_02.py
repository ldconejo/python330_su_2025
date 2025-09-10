from datetime import datetime
import os
import time
from typing import Annotated

import aiofiles
from fastapi import Depends, FastAPI, File, Form, Request, Response, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2_fragments.fastapi import Jinja2Blocks
from PIL import Image
from tinydb import TinyDB, Query

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Blocks(directory="templates")

def get_db():
    return TinyDB("db.json")

PHOTOS_PER_PAGE = 3

# Utility functions

def get_sorted_photos(all_photos, current_photo_count, new_photo_count):
    return sorted(all_photos,
                  key=lambda d: datetime.strptime(d["uploaded_at"], "%m/%d/%Y %I:%M:%S%p"),
                  reverse=True)[current_photo_count:new_photo_count]

def resize_image_for_web(photo_file_path):
    image_file = Image.open(f"static/{photo_file_path}")
    if image_file.width > image_file.height and image_file.width > 1920:
        image_file.thumbnail((1920, 1080))
    if image_file.width < image_file.height and image_file.width > 900:
        image_file.thumbnail((900, 1200))
    image_file.save(f"static{photo_file_path}")

# FastAPI routes

@app.get("/", response_class=HTMLResponse)
def photo_journal(request: Request, db: TinyDB = Depends(get_db)):
    sorted_photos = get_sorted_photos(db.all(), 0, PHOTOS_PER_PAGE)
    context = {
        "request": request,
        "photos": sorted_photos,
        "photo_count": PHOTOS_PER_PAGE,
    }
    return templates.TemplateResponse(name="photo_journal.html.jinja2", context=context)
