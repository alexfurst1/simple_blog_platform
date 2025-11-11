from fastapi import FastAPI, HTTPException
import json
from datetime import datetime

app = FastAPI()

file_path = "posts.json"
posts = []

def load_file(file_path):
    global posts
    try:
        with open(file_path,"r") as f:
            posts = json.load(f)
            print("data successfully loaded")
    except FileNotFoundError:
        print("file not found")
        posts = []
    except json.JSONDecodeError:
        print("file exists, but may be corrupted")
        posts = []

def save_file(file_path):
    global posts
    try:
        with open(file_path, "w") as f:
            json.dump(posts,f,indent=4)
            print("data successfully updated")
    except FileNotFoundError:
        print("file not found")
    except json.JSONDecodeError:
        print("json decode error")


@app.get("/") #root directory 
def root():
    return {"Hello world"}

#how to define a path in FastAPI
@app.get("/posts/{id}") # this is an app decorator, and defines a path for the HTTP GET method. The path is "/",
#which is our root directory
# REST read function
def get_post(id: int):
    load_file(file_path)
    for post in posts:
        if post["id"] == id:
            return post
    # return a blog post with a certain ID, or return all posts

@app.get("/posts")
def get_all(filter:str=None):
    load_file(file_path)
    if filter:
        filter = filter.lower()
        filtered_posts = [
            post for post in posts
            if filter in post["tags"]
        ]
        return filtered_posts
    return posts
            

@app.post("/posts")
def post_blog(title:str,content:str,category:str,tags:list[str]):
    timestamp = str(datetime.now())
    load_file(file_path)
    id = max([p["id"] for p in posts], default=0) + 1
    posts.append({"id":id,"title":title,"content":content,"category":category,"tags":tags,"createdAt":timestamp,"updatedAt":timestamp})
    save_file(file_path)
    print("blog posted successfully")
    return posts[-1]

@app.put("/posts/{id}")
def update_blog(id:int,new_title:str,new_content:str,new_category:str,new_tags:list):
    load_file(file_path)
    for post in posts:
        if post["id"] == id:
            post["title"] = new_title
            post["content"] = new_content
            post["category"] = new_category
            post["tags"] = new_tags
            post["updatedAt"] = str(datetime.now())
            save_file(file_path)
            return post
    


@app.delete("/posts/{id}")
def delete_post(id:int):
    load_file(file_path)
    for post in posts:
        if post["id"] == id:
            posts.remove(post)
    save_file(file_path)


    
