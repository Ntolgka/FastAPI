from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

# This creates the database tables if they don't exist already
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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


@ app.get("/")
def root():
    return {"message": "Hello World"}


@ app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@ app.get("/posts")
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@ app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)  # This adds the new post to the database
    db.commit()  # This commits the changes to the database
    db.refresh(new_post)  # This refreshes the new_post object with the new id
    return {"data": new_post}


# This must be above the get_post function because it can be confused with the get_post function (/latest is a valid id)
@ app.get("/posts/latest")
def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(
        models.Post.created_at.desc()).first()
    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are no posts yet")
    return {"data": latest_post}


@ app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"post_detail": post}


@ app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post.first()}
