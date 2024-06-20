import tempfile
from fastapi import File, UploadFile
import os


async def getInfo(file: UploadFile =  File(), prompt: str = "Simple and Straightforward Information"):
    try:
        with tempfile.NamedTemporaryFile() as tmp:
            temp_path = os.path.join(tmp.name, file.filename)

    except Exception as e:
        print(e)