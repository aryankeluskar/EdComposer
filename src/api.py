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
    allow_credentials=True
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
        model.add(str(contents))
        print("hello")
        ans = str(model.query("how to get into grad school?"))
        # delete the file after it's been processed
        os.remove(file.filename)
        print(ans)
            
            
    except Exception as e:
        print(e)
    finally:
        await file.close()

    return {'message': f'Successfuly processed {file.filename}', 'answer': ans}
