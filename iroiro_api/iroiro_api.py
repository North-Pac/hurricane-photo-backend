from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
  
@app.get('/login')
async def login():
    return {"login page test!": "welcome to the login page"}