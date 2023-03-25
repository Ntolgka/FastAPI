from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",  # This will add /posts to all the routes in this router
    tags=["posts"],
)


@ router.get("/", response_model=list[schemas.Post])
def posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)  # This adds the new post to the database
    db.commit()  # This commits the changes to the database
    db.refresh(new_post)  # This refreshes the new_post object with the new id
    return new_post


# This must be above the get_post function because it can be confused with the get_post function (/latest is a valid id)
@ router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    latest_post = db.query(models.Post).order_by(
        models.Post.created_at.desc()).first()
    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are no posts yet")
    return latest_post


@ router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return post


@ router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post.first()
