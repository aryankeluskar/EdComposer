from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from embedchain import App as llm
import os
from dotenv import load_dotenv

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
    root URL ("/"). The function is asynchronous, indicated by the `async` keyword before the
    function definition.
    ---
    Returns:
        FileResponse: A FileResponse object representing the "index.html" file.
    """
    return FileResponse("templates/index.html")


@app.post("/upload")
async def uploadInfo(
    file: UploadFile = File(),
    # prompt: str = "Simple and Straightforward Information",
):
    ans = None
    try:
        contents = await file.read()
        # print(content.)
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        model = llm()
        model.reset()

        print(file.filename)
        with open(file.filename, "wb") as f:
            f.write(contents)
            model.add(f.name)

        os.remove(f.name)
        
        querystr = """
THE MOST IMPORTANT THING IS TO RETURN ONLY TEXT THAT CAN BE PARSED AS JSON, IT NEEDS TO BE A VALID JSON STRING SO DO NOT INCLUDE ANY OTHER EXTRA INFORMATION AT ALL.
                You are an array generator that will return detailed information about a given topic in a json format.
                You will return NOTHING except a python list with json representing subtopics and containing details about the subtopic. The python list MUST have atleast 5 subtopics.
                Every subtopic must be an element of the list. Every subtopic must contain values for keys: image, title, details, narration.
                image is a detailed description of an image that can be best suited to explain the subtopic.
                title is 2-3 words for the subtopic.
                details is a detailed description of the subtopic, which is less than 50 words.
                narration is a detailed description of the subtopic, which is less than 100 words and covers the required information about the subtopic.
                The details should be strings and each string should be a complete sentence focusing on one idea.
                The format to be followed is [[<detail>,<detail>...],[<detail>,<detail>...]...]. The topic is
"""

        ans = model.query(querystr + "Aryan Keluskar")

        print(ans)

    except Exception as e:
        print(e)
    finally:
        await file.close()

    return {"message": f"Successfuly processed {file.filename}", "answer": ans}
