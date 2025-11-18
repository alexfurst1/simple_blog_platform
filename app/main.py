from fastapi import FastAPI, HTTPException
import json
from datetime import datetime
from fastapi import status
from app import schemas,crud,models,database
from .database import SessionLocal, engine, Base


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
@app.get("/posts/{id}",status_code=200, ) # this is an app decorator, and defines a path for the HTTP GET method. 
def get_post(post_id: int, db: Session = Depends(get_db)):


# example query parameter: localhost:9999/posts?filter=comedy

@app.get("/posts",status_code=200)
def get_all(filter:str=None):
    load_file(file_path)
    if filter:
        filtered_posts = [
            post for post in posts
            if any(filter.lower() in tag.lower() for tag in post["tags"])
        ]
        if not filtered_posts:
            raise HTTPException(status_code=404, detail="No posts matched that filter")
        return filtered_posts
    return posts
            

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def post_blog(post: BlogPost):
    timestamp = datetime.now().isoformat()
    load_file(file_path)
    new_id = max([p["id"] for p in posts], default=0) + 1
    new_post = {
        "id": new_id,
        "title": post.title,
        "content": post.content,
        "category": post.category,
        "tags": post.tags,
        "createdAt": timestamp,
        "updatedAt": timestamp,
    }
    posts.append(new_post)
    save_file(file_path)
    print("blog posted successfully")
    return new_post

@app.put("/posts/{id}",status_code=200)
def update_blog(id:int,post: BlogPost):
    load_file(file_path)
    for existing in posts:
        if existing["id"] == id:
            existing.update(post.model_dump())
            existing["updatedAt"] = datetime.now().isoformat()
            save_file(file_path)
            return existing
    raise HTTPException(status_code=404,detail= "Post not found")
    


@app.delete("/posts/{id}",status_code=204)
def delete_post(id:int):
    load_file(file_path)
    for post in posts:
        if post["id"] == id:
            posts.remove(post)
            save_file(file_path)
            return
    raise HTTPException(status_code=404,detail="Post not found")


    
