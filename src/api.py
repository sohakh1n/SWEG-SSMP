from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from PIL import Image
import os
from src.database import Database
import redis
from transformers import pipeline
import traceback

# API-Router
router = APIRouter()

# PostgreSQL-Datenbank
db = Database()

# Redis-Konfiguration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379)), db=0)

sentiment_analyzer = pipeline("sentiment-analysis")

text_generator = pipeline("text-generation", model="gpt2")

# Aktualisiere die Pfade
uploads_dir = "src/uploads"
full_size_dir = os.path.join(uploads_dir, "full")
reduced_size_dir = os.path.join(uploads_dir, "reduced")

# Verzeichnisse erstellen, falls sie nicht existieren
os.makedirs(full_size_dir, exist_ok=True)
os.makedirs(reduced_size_dir, exist_ok=True)

# Datenmodell für Posts
class PostBase(BaseModel):
    user: str
    text: Optional[str] = None
    image: Optional[str] = None

# Bild verkleinern
def resize_image(input_path, output_path, size=(800, 800)):
    with Image.open(input_path) as img:
        # Wenn das Bild einen Alpha-Kanal hat (RGBA), konvertiere es zu RGB
        if img.mode == "RGBA":
            img = img.convert("RGB")

        img.thumbnail(size)  # Bild verkleinern
        img.save(output_path, format="JPEG")  # Speichern als JPEG


@router.post("/api/v1/image")
async def upload_image(file: UploadFile):
    print("File received:", file.filename)  # Debug: Filename überprüfen
    print("Full Size Directory:", full_size_dir)
    print("Reduced Size Directory:", reduced_size_dir)
    try:
        full_path = os.path.abspath(os.path.join(full_size_dir, file.filename))
        print("Saving Full-Size Image to:", full_path)

        with open(full_path, "wb") as f:
            f.write(await file.read())

        print("Image saved successfully at:", full_path)

        # Reduced Image
        reduced_path = os.path.join(reduced_size_dir, file.filename)
        print("Saving Reduced-Size Image to:", reduced_path)
        resize_image(full_path, reduced_path)

        # Bildpfad zur Redis-Queue hinzufügen
        redis_client.lpush("image_queue", full_path)
        print("Image path pushed to Redis queue:", full_path)

        response = {
            "message": "Image uploaded successfully",
            "full_size_path": f"http://127.0.0.1:8000/uploads/full/{file.filename}",
            "reduced_size_path": f"http://127.0.0.1:8000/uploads/reduced/{file.filename}"
        }
        print("API Response:", response)  # Debug: Response überprüfen
        return response

    except Exception as e:
        print("Error saving image:", str(e))
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")


# GET /api/v1/image/{file_name} - Bild abrufen
@router.get("/api/v1/image/{file_name}")
def get_image(file_name: str):
    file_path = os.path.join(full_size_dir, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Image not found")

@router.post("/api/v1/post")
def create_post(post: PostBase):
    # Überprüfen, ob der Pfad bereits vollständig ist
    if not post.image.startswith("http"):
        post.image = f"http://127.0.0.1:8000{post.image}"
    print("Saving post with image path:", post.image)  # Debug-Ausgabe
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

@router.post("/sentiment")
async def analyze_sentiment(text: str):
    try:
        # Sentiment-Analyse ausführen
        result = sentiment_analyzer(text)
        return {
            "text": text,
            "sentiment": result[0]["label"],
            "score": result[0]["score"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during sentiment analysis: {str(e)}")


@router.post("/gpt")
async def generate_text(prompt: str, max_length: int = 50):
    """
    Generiert Text basierend auf einem Prompt.
    """
    try:
        # Textgenerierung mit GPT-2
        result = text_generator(prompt, max_length=max_length, num_return_sequences=1)
        return {"prompt": prompt, "generated_text": result[0]["generated_text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")