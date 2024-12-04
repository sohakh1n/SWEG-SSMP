import pytest
import os
import sys
from pathlib import Path
from src.database import Database

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))


@pytest.fixture
def db():
    """Create a temporary test database."""
    test_db = Database("test_social_media.db")
    yield test_db
    # Cleanup after tests
    if os.path.exists("test_social_media.db"):
        os.remove("test_social_media.db")


def test_database_creation(db):
    """Test if the database is created successfully."""
    assert os.path.exists("test_social_media.db")
    print("Database creation test passed!")


def test_add_post(db):
    """Test adding a post."""
    result = db.add_post(
        image_path="images/test.jpg",
        comment="Test post",
        username="testuser"
    )
    assert result > 0  # Should return the new post ID
    print("Add post test passed!")


def test_get_latest_post(db):
    """Test retrieving the latest post."""
    # Add posts
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

    # Get the latest post
    latest_post = db.get_latest_post()

    assert latest_post is not None
    assert latest_post['image_path'] == "images/test2.jpg"
    assert latest_post['comment'] == "Second post"
    assert latest_post['username'] == "user2"
    print("Get latest post test passed!")


def test_get_post_by_id(db):
    """Test retrieving a post by ID."""
    # Add a post
    post_id = db.add_post(
        image_path="images/test.jpg",
        comment="Test post",
        username="testuser"
    )
    # Get the post by ID
    post = db.get_post_by_id(post_id)

    assert post is not None
    assert post['id'] == post_id
    assert post['image_path'] == "images/test.jpg"
    assert post['comment'] == "Test post"
    assert post['username'] == "testuser"
    print("Get post by ID test passed!")


def test_search_posts(db):
    """Test searching for posts by username or comment."""
    # Add posts
    db.add_post(
        image_path="images/test1.jpg",
        comment="Hello world",
        username="user1"
    )
    db.add_post(
        image_path="images/test2.jpg",
        comment="Another post",
        username="user2"
    )

    # Search by username
    results = db.search_posts(query="user1")
    assert len(results) == 1
    assert results[0]['username'] == "user1"

    # Search by comment
    results = db.search_posts(query="Another")
    assert len(results) == 1
    assert results[0]['comment'] == "Another post"

    print("Search posts test passed!")
