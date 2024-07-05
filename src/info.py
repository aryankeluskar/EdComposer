from fastapi import File, UploadFile
from embedchain import App as llm
import os


async def getInfo(file: UploadFile = File(), prompt: str = "") -> str:
    rag_info = None

    # print("reached 1")

    try:
        contents = await file.read()
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        model = llm()
        model.reset()
        # print("reached 2")

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
        print(title_slide)

        # print("reached 2")

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
    ]

    red_color_dict = {
        "indian red": "#CD5C5C",
        "light coral": "#F08080",
        "salmon": "#FA8072",
        "dark salmon": "#E9967A",
        "light salmon": "#FFA07A",
        "crimson": "#DC143C",
        "red": "#FF0000",
        "firebrick": "#B22222",
        "dark red": "#8B0000",
    }

    pink_color_dict = {
        "pink": "#FFC0CB",
        "light pink": "#FFB6C1",
        "hot pink": "#FF69B4",
        "deep pink": "#FF1493",
        "medium violet red": "#C71585",
        "pale violet red": "#DB7093",
    }

    orange_color_dict = {
        "light salmon": "#FFA07A",
        "coral": "#FF7F50",
        "tomato": "#FF6347",
        "orange red": "#FF4500",
        "dark orange": "#FF8C00",
        "orange": "#FFA500",
    }

    yellow_color_dict = {
        "gold": "#FFD700",
        "yellow": "#FFFF00",
        "light yellow": "#FFFFE0",
        "lemon chiffon": "#FFFACD",
        "light goldenrod yellow": "#FAFAD2",
        "papaya whip": "#FFEFD5",
        "moccasin": "#FFE4B5",
        "peach puff": "#FFDAB9",
        "pale goldenrod": "#EEE8AA",
        "khaki": "#F0E68C",
        "dark khaki": "#BDB76B",
    }

    purple_color_dict = {
        "lavender": "#E6E6FA",
        "thistle": "#D8BFD8",
        "plum": "#DDA0DD",
        "violet": "#EE82EE",
        "orchid": "#DA70D6",
        "fuchsia": "#FF00FF",
        "magenta": "#FF00FF",
        "medium orchid": "#BA55D3",
        "medium purple": "#9370DB",
        "rebecca purple": "#663399",
        "blue violet": "#8A2BE2",
        "dark violet": "#9400D3",
        "dark orchid": "#9932CC",
        "dark magenta": "#8B008B",
        "purple": "#800080",
        "indigo": "#4B0082",
        "slate blue": "#6A5ACD",
        "dark slate blue": "#483D8B",
        "medium slate blue": "#7B68EE",
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

    blue_color_dict = {
        "Aqua": "#00FFFF",
        "Cyan": "#00FFFF",
        "LightCyan": "#E0FFFF",
        "PaleTurquoise": "#AFEEEE",
        "Aquamarine": "#7FFFD4",
        "Turquoise": "#40E0D0",
        "MediumTurquoise": "#48D1CC",
        "DarkTurquoise": "#00CED1",
        "CadetBlue": "#5F9EA0",
        "SteelBlue": "#4682B4",
        "LightSteelBlue": "#B0C4DE",
        "PowderBlue": "#B0E0E6",
        "LightBlue": "#ADD8E6",
        "SkyBlue": "#87CEEB",
        "LightSkyBlue": "#87CEFA",
        "DeepSkyBlue": "#00BFFF",
        "DodgerBlue": "#1E90FF",
        "CornflowerBlue": "#6495ED",
        "MediumSlateBlue": "#7B68EE",
        "RoyalBlue": "#4169E1",
        "Blue": "#0000FF",
        "MediumBlue": "#0000CD",
        "DarkBlue": "#00008B",
        "Navy": "#000080",
        "MidnightBlue": "#191970",
    }

    brown_color_dict = {
        "Cornsilk": "#FFF8DC",
        "BlanchedAlmond": "#FFEBCD",
        "Bisque": "#FFE4C4",
        "NavajoWhite": "#FFDEAD",
        "Wheat": "#F5DEB3",
        "BurlyWood": "#DEB887",
        "Tan": "#D2B48C",
        "RosyBrown": "#BC8F8F",
        "SandyBrown": "#F4A460",
        "Goldenrod": "#DAA520",
        "DarkGoldenrod": "#B8860B",
        "Peru": "#CD853F",
        "Chocolate": "#D2691E",
        "SaddleBrown": "#8B4513",
        "Sienna": "#A0522D",
        "Brown": "#A52A2A",
        "Maroon": "#800000",
    }

    # ask AI for color group

    color_group = model.query(
        "which color out of "
        + str(basic_colors)
        + " is most suitable for "
        + prompt
        + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
    )
    color_group = color_group.lower()
    color_group = color_group

    print("Color Group is" + color_group)

    # obtain recommended color group by asking AI to choose one out of the many in the color_group's dict
    recommended_bg_color = color_group
    hex_color = "default"

    if color_group == "red":
        recommended_bg_color = model.query(
            "which color out of "
            + str(red_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        if recommended_bg_color in red_color_dict.keys():
            hex_color = red_color_dict[recommended_bg_color]

    if color_group == "green":
        recommended_bg_color = model.query(
            "which color out of "
            + str(green_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        if recommended_bg_color in green_color_dict.keys():
            hex_color = green_color_dict[recommended_bg_color]

    if color_group == "blue":
        recommended_bg_color = model.query(
            "which color out of "
            + str(blue_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        if recommended_bg_color in blue_color_dict.keys():
            hex_color = blue_color_dict[recommended_bg_color]

    if color_group == "brown":
        recommended_bg_color = model.query(
            "which color out of "
            + str(brown_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        if recommended_bg_color in brown_color_dict.keys():
            hex_color = brown_color_dict[recommended_bg_color]

    if color_group == "purple":
        recommended_bg_color = model.query(
            "which color out of "
            + str(purple_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        if recommended_bg_color in purple_color_dict.keys():
            hex_color = purple_color_dict[recommended_bg_color]

    if color_group == "orange":
        recommended_bg_color = model.query(
            "which color out of "
            + str(orange_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        if recommended_bg_color in orange_color_dict.keys():
            hex_color = orange_color_dict[recommended_bg_color]

    if color_group == "yellow":
        recommended_bg_color = model.query(
            "which color out of "
            + str(yellow_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        if recommended_bg_color in yellow_color_dict.keys():
            hex_color = yellow_color_dict[recommended_bg_color]

    if color_group == "pink":
        recommended_bg_color = model.query(
            "which color out of "
            + str(pink_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        if recommended_bg_color in pink_color_dict.keys():
            hex_color = pink_color_dict[recommended_bg_color]

    recommended_fg_color = model.query(
        "If the background color is "
        + recommended_bg_color
        + " "
        + color_group
        + "then which color is most suitable foreground color for the text related to"
        + prompt
        + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
    )

    print(recommended_fg_color)

    if hex_color == "default":
        print("default encountered", recommended_bg_color)
        hex_color = "#000000"

    print(recommended_bg_color)
    print(str(hex_color))
    return str(hex_color)
