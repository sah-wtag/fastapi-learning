from typing import Annotated
from fastapi import HTTPException, status, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
)

# Dependencies
DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[
    schemas.TokenData,
    Depends(oauth2.get_current_user),
]


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: DBSession, current_user: CurrentUser):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No associated posts found"
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already voted on this post",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"Message": "Successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Message": "Successfully removed vote"}
