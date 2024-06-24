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

        recommended_bg_color = await getColor(model, prompt)

        title_slide = model.query(
            "Give me 2-3 words that form the best title slide for " + prompt
        )
        # title_slide = "Stanford"
        print(title_slide)

        # print(rag_info)
        return (rag_info, recommended_bg_color, title_slide)

    except Exception as e:
        print(e)
    finally:
        await file.close()


async def getColor(model, prompt) -> str:
    basic_colors = [
        "red",
        "pink",
        "orange",
        "yellow",
        "purple",
        "green",
        "blue",
        "brown",
        "white",
    ]

    red_color_dict = {
        "IndianRed": "#CD5C5C",
        "LightCoral": "#F08080",
        "Salmon": "#FA8072",
        "DarkSalmon": "#E9967A",
        "LightSalmon": "#FFA07A",
        "Crimson": "#DC143C",
        "Red": "#FF0000",
        "FireBrick": "#B22222",
        "DarkRed": "#8B0000",
    }

    pink_color_dict = {
        "Pink": "#FFC0CB",
        "LightPink": "#FFB6C1",
        "HotPink": "#FF69B4",
        "DeepPink": "#FF1493",
        "MediumVioletRed": "#C71585",
        "PaleVioletRed": "#DB7093",
    }

    orange_color_dict = {
        "LightSalmon": "#FFA07A",
        "Coral": "#FF7F50",
        "Tomato": "#FF6347",
        "OrangeRed": "#FF4500",
        "DarkOrange": "#FF8C00",
        "Orange": "#FFA500",
    }

    yellow_color_dict = {
        "Gold": "#FFD700",
        "Yellow": "#FFFF00",
        "LightYellow": "#FFFFE0",
        "LemonChiffon": "#FFFACD",
        "LightGoldenrodYellow": "#FAFAD2",
        "PapayaWhip": "#FFEFD5",
        "Moccasin": "#FFE4B5",
        "PeachPuff": "#FFDAB9",
        "PaleGoldenrod": "#EEE8AA",
        "Khaki": "#F0E68C",
        "DarkKhaki": "#BDB76B",
    }

    purple_color_dict = {
        "Lavender": "#E6E6FA",
        "Thistle": "#D8BFD8",
        "Plum": "#DDA0DD",
        "Violet": "#EE82EE",
        "Orchid": "#DA70D6",
        "Fuchsia": "#FF00FF",
        "Magenta": "#FF00FF",
        "MediumOrchid": "#BA55D3",
        "MediumPurple": "#9370DB",
        "RebeccaPurple": "#663399",
        "BlueViolet": "#8A2BE2",
        "DarkViolet": "#9400D3",
        "DarkOrchid": "#9932CC",
        "DarkMagenta": "#8B008B",
        "Purple": "#800080",
        "Indigo": "#4B0082",
        "SlateBlue": "#6A5ACD",
        "DarkSlateBlue": "#483D8B",
        "MediumSlateBlue": "#7B68EE",
    }

    green_color_dict = {
        "GreenYellow": "#ADFF2F",
        "Chartreuse": "#7FFF00",
        "LawnGreen": "#7CFC00",
        "Lime": "#00FF00",
        "LimeGreen": "#32CD32",
        "PaleGreen": "#98FB98",
        "LightGreen": "#90EE90",
        "MediumSpringGreen": "#00FA9A",
        "SpringGreen": "#00FF7F",
        "MediumSeaGreen": "#3CB371",
        "SeaGreen": "#2E8B57",
        "ForestGreen": "#228B22",
        "Green": "#008000",
        "DarkGreen": "#006400",
        "YellowGreen": "#9ACD32",
        "OliveDrab": "#6B8E23",
        "Olive": "#808000",
        "DarkOliveGreen": "#556B2F",
        "MediumAquamarine": "#66CDAA",
        "DarkSeaGreen": "#8FBC8B",
        "LightSeaGreen": "#20B2AA",
        "DarkCyan": "#008B8B",
        "Teal": "#008080",
    }

    recommended_bg_color = model.query(
        "which color out of "
        + str(basic_colors)
        + " is most suitable for "
        + prompt
        + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
    )
    print(recommended_bg_color)

    return str(recommended_bg_color)
