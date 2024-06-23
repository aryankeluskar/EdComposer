from fastapi import File, UploadFile


async def getInfo(
    file: UploadFile = File(), prompt: str = "Simple and Straightforward Information"
):
    pass
