import tempfile
from fastapi import File, UploadFile
import os


async def getInfo(file: UploadFile =  File(), prompt: str = "Simple and Straightforward Information"):
    pass