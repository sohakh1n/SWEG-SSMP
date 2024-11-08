import sqlite3
from pathlib import Path
import os
from datetime import datetime

class Database:
    def __init__(self, db_name="social_media.db"):
        """Initialize database connection"""
        self.db_name = db_name
        self.conn = None
        self.create_tables()

    def connect(self):
        """Create a database connection"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            return self.conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def create_tables(self):
        """Create posts table if it doesn't exist"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            comment TEXT,
            username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            conn = self.connect()
            if conn:
                conn.execute(create_table_sql)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            if conn:
                conn.close()

    def add_post(self, image_path: str, comment: str, username: str) -> bool:
        """
        Add a new post to the database
        Returns True if successful, False otherwise
        """
        sql = """
        INSERT INTO posts (image_path, comment, username, created_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP);
        """
        try:
            conn = self.connect()
            if conn:
                conn.execute(sql, (image_path, comment, username))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error adding post: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_latest_post(self) -> dict:
        """Retrieve the most recent post"""
        sql = """
        SELECT id, image_path, comment, username, created_at
        FROM posts
        ORDER BY id DESC
        LIMIT 1;
        """
        try:
            conn = self.connect()
            if conn:
                cursor = conn.execute(sql)
                row = cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'image_path': row[1],
                        'comment': row[2],
                        'username': row[3],
                        'created_at': row[4]
                    }
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving latest post: {e}")
            return None
        finally:
            if conn:
                conn.close()