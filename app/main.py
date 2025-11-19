from fastapi import FastAPI, HTTPException
from fastapi import status
from app import schemas,crud
from .database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from fastapi import Depends



app = FastAPI()

Base.metadata.create_all(bind=engine) #Creates all database tables that are defined in my SQLAlchemy models if they don’t already exist.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/") #root directory 
def root():
    return {"message":"Hello world"}

#how to define a path in FastAPI
@app.get("/posts/{id}",status_code=200, response_model=schemas.BlogPostRead) # this is an app decorator, and defines a path for the HTTP GET method. 
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, id)
    if not post:
        raise HTTPException(status_code=404,details="post not found")
    return post

# example query parameter: localhost:9999/posts?filter=comedy

@app.get("/posts",status_code=200, response_model=list[schemas.BlogPostRead])
def get_all(category:str=None, db: Session = Depends(get_db)):
    return crud.get_posts(db,category)    
    
            

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def post_blog(post: schemas.BlogPostCreate, db : Session = Depends(get_db)):
    crud.post_blog(db, post)

@app.put("/posts/{id}",status_code=200)
def update_blog(id:int,updated_post: schemas.BlogPostCreate, db: Session = Depends(get_db)):
    post = crud.update_blog(db, id, updated_post)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post
    


@app.delete("/posts/{id}",status_code=204)
def delete_post(id:int, db : Session = Depends(get_db)):
    post = crud.delete_post(db,id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post

    
