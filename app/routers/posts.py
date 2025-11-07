from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, author_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == author_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db_post = models.Post(**post.model_dump(), author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/", response_model=List[schemas.PostWithAuthor])
def get_posts(
    skip: int = 0,
    limit: int = 100,
    published: Optional[int] = None,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Post)

    if published is not None:
        query = query.filter(models.Post.published == published)

    if author_id is not None:
        query = query.filter(models.Post.author_id == author_id)

    posts = query.offset(skip).limit(limit).all()
    return posts


@router.get("/{post_id}", response_model=schemas.PostWithAuthor)
def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return db_post


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    update_data = post.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    db.delete(db_post)
    db.commit()
    return None
