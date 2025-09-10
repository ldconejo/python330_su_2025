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

@app.post("/post-photo", response_class=HTMLResponse)
async def post_photo(request: Request, entry: Annotated[str, Form()], photo_upload: UploadFile,
                     db: TinyDB = Depends(get_db)):
    valid_image_file = True
    photo_file_path = f"/images/{photo_upload.filename}"
    async with aiofiles.open(f"static{photo_file_path}", "wb") as out_file:
        content = await photo_upload.read()
        await out_file.write(content)
        try:
            with Image.open(f"static{photo_file_path}") as image_file:
                image_file.verify()
        except (IOError, SyntaxError):
            valid_image_file = False
            os.remove(f"static{photo_file_path}")
    if valid_image_file:
        resize_image_for_web(photo_file_path)
        uploaded_at = time.strftime("%m/%d/%Y %I:%M:%S%p")
        db.insert({"entry": entry,
                   "file_path": photo_file_path,
                   "uploaded_at": uploaded_at})
    sorted_photos = get_sorted_photos(db.all(), 0, PHOTOS_PER_PAGE)
    context = {
        "request": request,
        "photos": sorted_photos,
        "photo_count": PHOTOS_PER_PAGE,
        "invalid_image_file": not valid_image_file,
    }
    return templates.TemplateResponse(name="photo_journal.html.jinja2", context=context, block_name="photos")