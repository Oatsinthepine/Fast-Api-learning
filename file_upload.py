from fastapi import FastAPI, UploadFile

# Here is the way to change the default file upload limit in FastAPI
from starlette.formparsers import MultiPartParser

MultiPartParser.max_part_size = 1024 * 1024 * 10  # Set to 10 MB, or whatever limit you prefer

app = FastAPI()

"""
file upload in FastAPI
- Different Techniques
- How they works
- Best Practices
"""

@app.post("/upload")
async def endpoint(upload_file: UploadFile):
    """
    Example endpoint to handle file upload. Use this way to upload small files, not for large files. As this method reads the entire file into memory.
    :param upload_file:
    :return:
    """
    print(upload_file.file)
    # this is checking if the uploaded file is in memory or not, if the uploaded file is greater than default limit, it will be stored in disk, otherwise it will be stored on memory.
    print(upload_file._in_memory)
    content = await upload_file.read()
    print(content)

@app.post("/upload2")
async def endpoint2(upload_file: UploadFile):
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