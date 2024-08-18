import json
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

from src.info import getInfo
from src.images import getImages
from src.voice import generate_voice

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# put everything in /templates folder for fastapi
current_dir = os.path.dirname(os.path.abspath(__file__))
print("=" * 20)
print(current_dir)
app.mount(
    "/templates", StaticFiles(directory=current_dir + "/templates"), name="templates"
)
app.mount(
    "/homepage_files",
    StaticFiles(directory=current_dir + "/homepage_files"),
    name="homepage_files",
)


@app.get("/edcomposer")
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
    # print list of files in templates directory
    # return os.listdir()
    return FileResponse(current_dir + "/templates/edcomposer.html")


@app.post("/edcomposer/upload")
async def uploadInfo(
    file: UploadFile = File(),
    prompt: Annotated[str, Form()] = "",
):
    result_getInfo = await getInfo(file, prompt)
    print(result_getInfo)
    # print(result_getInfo)

    answer = result_getInfo[0]
    slides_bg_colors = result_getInfo[1]
    slides_fg_colors = result_getInfo[2]
    title_slide_text = result_getInfo[3]

    # convert answer which is a str, to a json object
    answer = json.loads(answer)

    USE_TEST_DATA = False
    if USE_TEST_DATA:
        # use the json object in sample.json as test data
        with open("sample.json", "r") as f:
            answer = json.load(f)

    # for i in answer:
    #     print(i['details'])

    img_list = await getImages(answer)
    print(img_list)

    title_json = {
        "title": title_slide_text,
        "slides_bg_colors": slides_bg_colors,
        "slides_fg_colors": slides_fg_colors,
        "narration": "Let's explore " + title_slide_text,
    }

    for ind, i in enumerate(answer):
        i["image"] = img_list.pop(0)
        print(i["details"])
        await generate_voice(i["details"], ind)

    return {
        "message": f"Successfuly processed {file.filename}",
        "title": title_slide_text,
        "slides_bg_colors": slides_bg_colors,
        "slides_fg_colors": slides_fg_colors,
        "images": img_list,
        "answer": answer,
    }
