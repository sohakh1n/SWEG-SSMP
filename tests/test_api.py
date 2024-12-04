from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_post():
    response = client.post("/api/v1/post", json={"user": "testuser", "text": "Hello world"})
    assert response.status_code == 200
    assert response.json()["message"] == "Post created successfully"

def test_get_latest_post():
    client.post("/api/v1/post", json={"user": "testuser", "text": "Latest post"})
    response = client.get("/api/v1/post/latest")
    assert response.status_code == 200
    assert response.json()["text"] == "Latest post"

def test_upload_image():
    with open("test_image.jpg", "wb") as f:
        f.write(b"test image data")
    with open("test_image.jpg", "rb") as f:
        response = client.post("/api/v1/image", files={"file": f})
    assert response.status_code == 200
    assert "Image uploaded successfully" in response.json()["message"]
