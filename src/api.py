from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from src.database import Database

# API-Router
router = APIRouter()

# PostgreSQL-Datenbank
db = Database()

# Upload-Verzeichnis für Bilder
images_dir = "uploads"
os.makedirs(images_dir, exist_ok=True)

# Datenmodell für Posts
class PostBase(BaseModel):
    user: str
    text: Optional[str] = None
    image: Optional[str] = None

# POST /api/v1/image - Bild hochladen
@router.post("/api/v1/image")
async def upload_image(file: UploadFile):
    file_path = os.path.join(images_dir, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"message": "Image uploaded successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

# GET /api/v1/image/{file_name} - Bild abrufen
@router.get("/api/v1/image/{file_name}")
def get_image(file_name: str):
    file_path = os.path.join(images_dir, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Image not found")

# POST /api/v1/post - Post erstellen
@router.post("/api/v1/post")
def create_post(post: PostBase):
    post_id = db.add_post(post.image, post.text, post.user)
    return {"id": post_id, "message": "Post created successfully"}

# GET /api/v1/post/latest - Neuesten Post abrufen
@router.get("/api/v1/post/latest")
def get_latest_post():
    post = db.get_latest_post()
    if not post:
        raise HTTPException(status_code=404, detail="No posts found")
    return post

# GET /api/v1/post/search/{query} - Posts durchsuchen
@router.get("/api/v1/post/search/{query}")
def search_posts(query: str):
    results = db.search_posts(query)
    return results
