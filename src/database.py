from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Absoluten Pfad zur Datenbankdatei festlegen
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'social_media.db')}"

# Engine erstellen
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Tabellenmodell
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=True)
    comment = Column(Text, nullable=True)
    username = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# Datenbank initialisieren
def init_db():
    Base.metadata.create_all(bind=engine)

# Datenbankoperationen
class Database:
    def __init__(self):
        self.db = SessionLocal()

    def add_post(self, image_path: str, comment: str, username: str) -> int:
        new_post = Post(image_path=image_path, comment=comment, username=username)
        self.db.add(new_post)
        self.db.commit()
        self.db.refresh(new_post)
        return new_post.id

    def get_latest_post(self):
        return self.db.query(Post).order_by(Post.created_at.desc()).first()

    def get_post_by_id(self, post_id: int):
        return self.db.query(Post).filter(Post.id == post_id).first()

    def search_posts(self, query: str):
        return self.db.query(Post).filter(
            (Post.comment.ilike(f"%{query}%")) | (Post.username.ilike(f"%{query}%"))
        ).all()
