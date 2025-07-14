from fastapi import FastAPI, UploadFile
# this CORS middleware is used to allow cross-origin requests, which is useful when your frontend and backend are hosted on different domains or ports.
from fastapi.middleware.cors import CORSMiddleware
# Here is the way to change the default file upload limit in FastAPI
from starlette.formparsers import MultiPartParser
from pathlib import Path
from typing import List

MultiPartParser.max_part_size = 1024 * 1024 * 10  # Set to 10 MB, or whatever limit you prefer


# define the directory when received files from the frontend uploaded to be stored
UPLOAD_DIR = Path("uploads")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # Allows all origins, you can specify a list of allowed origins
    allow_credentials = True,
    allow_methods = ["*"],  # Allows all methods, you can specify a list of allowed methods
    allow_headers = ["*"],  # Allows all headers, you can specify a list of allowed headers
)


"""
file upload in FastAPI
- Different Techniques
- How they works
- Best Practices
"""

@app.get("/")
def index_page() -> dict:
    return {"Welcome": "You have entered the file-upload backend home page!"}


@app.post("/upload")
async def endpoint(upload_file: UploadFile) -> None:
    """
    Example endpoint to handle file upload. Use this way to upload small files, not for large files. As this method reads the entire file into memory.
    :param upload_file:
    :return: None
    """
    print(upload_file.file)
    # this is checking if the uploaded file is in memory or not, if the uploaded file is greater than default limit, it will be stored in disk, otherwise it will be stored on memory.
    print(upload_file._in_memory)
    content = await upload_file.read()
    print(content)

@app.post("/upload2")
async def endpoint2(upload_file: UploadFile) -> None:
    """
    Example endpoint to handle file upload. Use this way to upload large files, as this method streams the file in chunks.
    :param upload_file:
    :return:
    """
    with open(upload_file.filename, "wb") as f:
        while True:
            chunk = await upload_file.read(1024 * 1024)
            if not chunk:
                break
            print(chunk)

@app.post("/upload_file")
async def create_upload_file(file_uploads: List[UploadFile]) -> dict:
    """
    This is the api endpoint to receive multiple files from the frontend.
    :param file_uploads:
    :return: dict
    """
    for file_upload in file_uploads:
        content = await file_upload.read()
        with open(UPLOAD_DIR/file_upload.filename, "wb") as f:
            f.write(content)

    return {"filename": [f.filename for f in file_uploads], "content_type": [f.content_type for f in file_uploads]}


