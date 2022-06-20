from fastapi import FastAPI


app = FastAPI()
"""
This is an instance of the FastAPI class
providing access to all methods of the FastAPI class
"""

"""
Each of the HTTP methods is called an "operation"

POST: to create data
GET: to read data
PUT: to update data
DELETE: to delete data

Example:
Sending a GET request to 'http://127.0.0.1:8000/' will call the @app.get("/") root decorated method
Sending a GET request to 'http://127.0.0.1:8000/login' will call the @app.get("/login") login method
"""


# Basic endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/login')
async def login():
    return {"login page": "welcome to the login page"}


@app.get('/gallery')
async def gallery():
    return {"the gallery": "here you can see photos uploaded by all users"}


@app.get('/upload')
async def upload():
    return {"upload page": "Here you can upload new photos once logged in"}


@app.get('/mypage')
async def mypage():
    return {"mypage": "Here you view all photos you have uploaded"}
