from fastapi import APIRouter, HTTPException
from src.database import Database
from src.models import Post

router = APIRouter()
db = Database()

@router.post("/posts", response_model=dict)
def create_post(post: Post):
    success = db.add_post(post.image_path, post.comment, post.username)
    if not success:
        raise HTTPException(status_code=500, detail="Post could not be created.")
    return {"message": "Post created successfully"}

@router.get("/posts/{id}", response_model=dict)
def get_post(id: int):
    post = db.get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return post

@router.get("/posts", response_model=list)
def search_posts(username: str = None, comment: str = None):
    return db.search_posts(username, comment)

