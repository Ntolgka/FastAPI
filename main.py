from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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
    return {"data": my_posts}


@ app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# This must be above the get_post function because it can be confused with the get_post function (/latest is a valid id)
@ app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}


@ app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"post_detail": post}


@ app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_dict = post.dict()
    post_dict["id"] = id
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    my_posts.remove(post)
    my_posts.append(post_dict)
    return {"data": post_dict}
