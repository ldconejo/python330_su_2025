import io
from fastapi.testclient import TestClient
from main import app
from tinydb import TinyDB

client = TestClient(app)


def test_post_photo_invalid_image(tmp_path, monkeypatch):
    db_path = tmp_path / "test_db.json"
    db = TinyDB(db_path)
    monkeypatch.setattr("main.get_db", lambda: db)

    # Fake "text file" instead of image
    file_content = io.BytesIO(b"not an image at all")
    files = {"photo_upload": ("fake.txt", file_content, "text/plain")}
    data = {"entry": "Bad file"}

    resp = client.post("/post-photo", data=data, files=files)
    assert resp.status_code == 200
    text = resp.text
    assert "invalid_image_file" in text or "Bad file" not in text
    assert db.all() == []  # Should not insert invalid entries
