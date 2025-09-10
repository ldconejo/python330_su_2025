@app.post("/post-photo", response_class=HTMLResponse)
async def post_photo(request: Request, entry: Annotated[str, Form()], photo_upload: UploadFile,
                     db: TinyDB = Depends(get_db)):
    valid_image_file = True
    photo_file_path = f"/images{photo_upload.filename}"
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