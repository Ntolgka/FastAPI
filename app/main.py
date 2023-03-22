from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='fastapi', user='postgres', password='password123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()  # to execute sql statements
        print("Connected to database")
        break
    except Exception as error:
        print("Connection to database failed dur to:", error)
        time.sleep(5)

my_posts = [{"id": 1, "title": "Hello World 1", "content": "This is my first post"},
            {"id": 2, "title": "Hello World 2",
                "content": "This is my second post"},
            {"id": 3, "title": "Hello World 3", "content": "This is my third post"},
            {"id": 4, "title": "Hello World 4", "content": "This is my fourth post"}]


def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


@ app.get("/")
def root():
    return {"message": "Hello World"}


@ app.get("/posts")
def posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@ app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# This must be above the get_post function because it can be confused with the get_post function (/latest is a valid id)
@ app.get("/posts/latest")
def get_latest_post():
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 1")
    post = cursor.fetchone()
    return {"data": post}


@ app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"post_detail": post}


@ app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    return {"data": updated_post}
