from typing import List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database


router = APIRouter(
    prefix="/comment",
    tags=["Comments"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comment(comment: schemas.Comment, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(
        models.Post.id == comment.post_id).first()
    if not post:  # if post does not exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {comment.post_id} not found")

    new_comment = models.Comment(
        user_id=current_user.id, post_id=comment.post_id, content=comment.content)

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/{id}", response_model=List[schemas.CommentOut])
def get_comments(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(
        models.Post.id == id).first()

    if not post:  # if post does not exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    comments = db.query(
        models.Comment, models.User).join(
        models.User, models.Comment.user_id == models.User.id).filter(
        models.Comment.post_id == id).all()

    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no comments for the post with id: {id}")

    comment_outs = [
        schemas.CommentOut(
            id=comment.id,
            content=comment.content,
            created_at=comment.created_at,
            owner=schemas.UserComment(
                id=user.id,
                email=user.email,
                username=user.username
            )
        ) for comment, user in comments
    ]

    return comment_outs


@ router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id: {id} not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not allowed to delete this comment")

    comment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ router.put("/{id}", response_model=schemas.CommentOut, status_code=status.HTTP_202_ACCEPTED)
def update_comment(id: int, updated_comment: schemas.CommentUpdate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id: {id} not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not allowed to update this comment")

    comment_query.update({"content": updated_comment.content})
    db.commit()
    return comment
