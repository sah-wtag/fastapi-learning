from random import randrange
import stat
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None


my_posts = [
    {"title": "We are new post", "id": 1, "content": "This is our content"},
    {"title": "We are 2nd post", "id": 2, "content": "This is our 2nd content"},
]


def find_post(post_id):
    for p in my_posts:
        if p["id"] == post_id:
            return p


def find_index_post(post_id):
    for i, p in enumerate(my_posts):
        if p["id"] == post_id:
            return i


@app.get("/")
def root():
    return {"message": "Welcome to a new fastapi projects"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/latest")
def latest_posts():
    post = my_posts[-1]
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return {"post_details": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return my_posts[index]
