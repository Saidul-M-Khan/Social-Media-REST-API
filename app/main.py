from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        connection = psycopg2.connect(host='localhost', database='FastAPI_SocialMedia', user='postgres', password='1980',   cursor_factory=RealDictCursor)
        cursor=connection.cursor()
        print('Database is connected!')
        break
    except Exception as error:
        print('Database connection failed!')
        print('Error: ', error)
        time.sleep(2)

#* Root
@app.get("/")
async def root():
    return {"message": "Server is up and running!"}

@app.get("/sqlalchemy")
async def alchemy(db: Session = Depends(get_db)):
    return {"status": "Success!"}

#* Create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connection.commit()  # Commit the change
    return {"data": new_post}

#* Get all posts
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    connection.commit()  # Commit the change
    return {"data": posts}

#* Get a post by id
@app.get("/posts/{id}")
def get_single_post(id: str):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (id, ))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    connection.commit()  # Commit the change
    return {"data": post}

#* Delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    connection.commit()  # Commit the change
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#* Update post
@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: str, post: Post):
    cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    connection.commit()  # Commit the change
    return {"data": updated_post}