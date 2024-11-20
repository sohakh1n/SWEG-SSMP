from pydantic import BaseModel

class Post(BaseModel):
    image_path: str
    comment: str
    username: str
