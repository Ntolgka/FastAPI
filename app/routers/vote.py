from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database


router = APIRouter(
    prefix="/vote",
    tags=["Votes"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:  # if post does not exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id ==
                                              vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):  # if vote is upvote
        if found_vote:  # if user has already voted for post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted for post {vote.post_id}")

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return Response("Successfully added vote", status_code=status.HTTP_201_CREATED)
    else:  # if vote is downvote
        if not found_vote:  # if user has not voted for post
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return Response("Successfully removed vote", status_code=status.HTTP_200_OK)
