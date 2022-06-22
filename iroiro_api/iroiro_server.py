import boto3
import psycopg2

from typing import List
from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI, UploadFile

from fastapi.middleware.cors import CORSMiddleware

from colorizer_app import Colorizer

S3_BUCKET_NAME = "iro-bucket"


class PhotoModel(BaseModel):
    id: int
    photo_name: str
    photo_url: str
    


app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status")
async def check_status():
    return "Hello World!"


@app.get("/photos", response_model=List[PhotoModel])##consider calling the colorizer here
async def get_all_photos():
    # Connect to our database
    conn = psycopg2.connect(
        database="irodb", user="docker", password="docker", host="0.0.0.0"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM photo ORDER BY id DESC")
    rows = cur.fetchall()

    formatted_photos = []
    for row in rows:
        formatted_photos.append(
            PhotoModel(
                id=row[0], photo_name=row[1], photo_url=row[2]
            )
        )

    cur.close()
    conn.close()
    return formatted_photos


@app.post("/photos", status_code=201)
async def add_photo(file: UploadFile):## consider calling the colorizer here before the post occurs
    print("Endpoint hit!!")
    print(file.filename)
    print(file.content_type)

    # Upload file to AWS S3
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={"ACL": "public-read"})

    uploaded_file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}"

    # Store URL in database
    conn = psycopg2.connect(
        database="irodb", user="docker", password="docker", host="0.0.0.0"
    )
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO photo (photo_name, photo_url) VALUES ('{file.filename}', '{uploaded_file_url}' )"
    )
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)