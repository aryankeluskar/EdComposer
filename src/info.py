from fastapi import File, UploadFile
from embedchain import App as llm
import os


async def getInfo(file: UploadFile = File(), prompt: str = "") -> str:
    rag_info = None

    try:
        contents = await file.read()
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
                You will return NOTHING except a python list with json representing subtopics and containing details about the subtopic. The python list MUST have 6 to 10 subtopics 
                depending on how detailed one has to go in order to grasp the topic in its entirety. 
                Every subtopic must be an element of the list. Every subtopic must contain values for keys: image, title, details, narration.
                image is a detailed description of an image that can be best suited to explain the subtopic.
                title is 2-3 words for the subtopic.
                details is a detailed description of the subtopic, which is more than 20 words.
                narration is a detailed description of the subtopic, which is less than 100 words and covers the required information about the subtopic.
                The details should be strings and each string should be a complete sentence focusing on one idea.
                The format to be followed is [[<detail>,<detail>...],[<detail>,<detail>...]...]. The topic is
                """

        rag_info = model.query(querystr + prompt)

        recommended_bg_color = model.query("which color does "+prompt+" use the most? YOU MUST ONLY RETURN THE HTML CODE OF THE COLOR WHICH IS LIGHT AND MOST SUITED FOR THE BRAND, AND NO OTHER TEXT")
        print(recommended_bg_color)

        title_slide = "Stanford"

        # print(rag_info)
        return (rag_info, recommended_bg_color, title_slide)

    except Exception as e:
        print(e)
    finally:
        await file.close()


