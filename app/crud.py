# holds all CRUD logic
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models,schemas,database,main
from datetime import datetime

def root():
    return {"message":"Hello world"}

def get_post(db : Session, id: int):
    return (
        db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
    )

def get_posts(db: Session, filter:str=None):
    query = db.query(models.BlogPost)

    if filter:
        query = query.filter(models.BlogPost.category == filter)

    return query.all

def post_blog(db: Session, post: schemas.BlogPostCreate):
    db_post = models.BlogPost(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
    

def update_blog(db: Session, id:int, updated: schemas.BlogPostCreate):
    db_post = get_post(db, id)
    if db_post is None:
        return None
    
    db_post.title = updated.title
    db_post.content = updated.content
    db_post.category = updated.category
    db_post.tags = updated.tags

    db.commit()
    db.refresh(db_post)
    return db_post

    

def delete_post(db : Session, id:int):
    db_post = get_post(db, id)
    if db_post is None:
        return None
    
    db.delete(db_post)
    db.commit()
    
    return db_post
