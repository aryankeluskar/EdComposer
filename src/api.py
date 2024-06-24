import json
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from info import getInfo
from images import getImages

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
async def root():
    r"""
    ### Root Endpoint
    A function that serves the root endpoint of the API. It returns a FileResponse object that
    represents the "index.html" file located in the "templates" directory. This function is
    decorated with the `@app.get("/")` decorator, which means it will handle GET requests to the
    root URL ("/").
    ---
    Returns:
        FileResponse: A FileResponse object representing the "index.html" file.
    """
    return FileResponse("templates/index.html")


@app.post("/upload")
async def uploadInfo(
    file: UploadFile = File(),
    prompt: Annotated[str, Form()] = "",
):
    answer = await getInfo(file, prompt)
    # convert answer which is a str, to a json object
    answer = json.loads(answer)

    # a json object is in sample.json, bring it out and put in answer
    # with open("sample.json", "r") as f:
    #     answer = json.load(f)

    # for i in answer:
    #     print(i['details'])

    print(answer)

    img_list = await getImages(answer)
    print(img_list)

    return {"message": f"Successfuly processed {file.filename}", "answer": answer}
