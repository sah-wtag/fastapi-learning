from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app import oauth2
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


# Dependencies
DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[
    schemas.TokenData,
    Depends(oauth2.get_current_user),
]


# --------------------------------------------------
# GET ALL POSTS by logged in user
# --------------------------------------------------
@router.get(
    "/",
    response_model=list[schemas.PostResponse],
)
def get_posts(
    db: DBSession,
    current_user: CurrentUser,
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(
            models.Post.owner_id == current_user.id
            and models.Post.title.contains(search)
        )
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


# --------------------------------------------------
# GET ALL POSTS
# --------------------------------------------------
@router.get(
    "/all",
    response_model=list[schemas.PostResponse],
)
def get_all_posts(
    db: DBSession,
    current_user: CurrentUser,
):
    posts = db.query(models.Post).all()
    return posts


# --------------------------------------------------
# GET LATEST POST
# --------------------------------------------------
@router.get(
    "/latest",
    response_model=schemas.PostResponse,
)
def latest_posts(
    db: DBSession,
):
    latest = db.query(models.Post).order_by(models.Post.created_at.desc()).first()

    if latest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found",
        )

    return latest


# --------------------------------------------------
# TEST SQLALCHEMY
# --------------------------------------------------
@router.get("/sqlalchemy")
def test_posts(
    db: DBSession,
):
    posts = db.query(models.Post).all()
    return posts


# --------------------------------------------------
# GET SINGLE POST
# --------------------------------------------------
@router.get(
    "/{id}",
    response_model=schemas.PostResponse,
)
def get_post(
    id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to Perform this actions",
        )

    return post


# --------------------------------------------------
# CREATE POST
# --------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def create_post(
    post: schemas.CreatePost,
    db: DBSession,
    current_user: CurrentUser,
):
    new_post = models.Post(
        owner_id=current_user.id,
        **post.model_dump(),
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# --------------------------------------------------
# DELETE POST
# --------------------------------------------------
@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
    id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to Perform this actions",
        )

    post_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --------------------------------------------------
# UPDATE POST
# --------------------------------------------------
@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PostResponse,
)
def update_post(
    id: int,
    post: schemas.CreatePost,
    db: DBSession,
    current_user: CurrentUser,
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to Perform this actions",
        )

    post_query.update(
        post.model_dump(),
        synchronize_session=False,
    )

    db.commit()

    return post_query.first()
