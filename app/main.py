from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@ app.get("/")
def root():
    return {"message": "Hello World"}
