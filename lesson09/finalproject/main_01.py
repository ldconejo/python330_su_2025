from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def photo_journal():
    return {"message": "Hello Photo Journal!"}
