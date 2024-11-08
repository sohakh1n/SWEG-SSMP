import pytest
import os
import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.database import Database

@pytest.fixture
def db():
    """Create a temporary test database"""
    test_db = Database("test_social_media.db")
    yield test_db
    # Cleanup after tests
    if os.path.exists("test_social_media.db"):
        os.remove("test_social_media.db")

def test_database_creation(db):
    """Test if database is created successfully"""
    assert os.path.exists("test_social_media.db")
    print("Database creation test passed!")  # Added print statement

def test_add_post(db):
    """Test adding a post"""
    result = db.add_post(
        image_path="images/test.jpg",
        comment="Test post",
        username="testuser"
    )
    assert result is True
    print("Add post test passed!")  # Added print statement

def test_get_latest_post(db):
    """Test retrieving the latest post"""
    # Add a post first
    db.add_post(
        image_path="images/test1.jpg",
        comment="First post",
        username="user1"
    )
    db.add_post(
        image_path="images/test2.jpg",
        comment="Second post",
        username="user2"
    )
    
    # Get latest post
    latest_post = db.get_latest_post()
    
    assert latest_post is not None
    assert latest_post['image_path'] == "images/test2.jpg"
    assert latest_post['comment'] == "Second post"
    assert latest_post['username'] == "user2"
    print("Get latest post test passed!")  # Added print statement