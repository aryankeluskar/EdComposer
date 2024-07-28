from fastapi import File, UploadFile
from embedchain import App as llm
import os

import requests


async def getInfo(file: UploadFile = File(), prompt: str = "") -> str:
    rag_info = None

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

    response = requests.post(
        "https://gateway.ai.cloudflare.com/v1/"
        + os.getenv("CLOUDFLARE_ACCOUNT_ID")
        + "/"
        + os.getenv("CLOUDFLARE_GATEWAY_ID")
        + "/openai/chat/completions",
        headers={
            "Authorization": "Bearer " + os.getenv("CLOUDFLARE_OPENAI_TOKEN"),
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "What is Cloudflare"}],
        },
    )

    print(response.json())

    result_getColor = await getColor(model, prompt)
    recommended_bg_color = result_getColor[0]
    recommended_fg_color = result_getColor[1]

    title_slide = model.query(
        "Give me 2-3 words that form the best title slide for " + prompt
    )
    print(title_slide)

    # print("reached 2")

    await file.close()

    # print(rag_info)
    return (rag_info, recommended_bg_color, recommended_fg_color, title_slide)


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
        "greenyellow": "#ADFF2F",
        "chartreuse": "#7FFF00",
        "lawn green": "#7CFC00",
        "lime": "#00FF00",
        "lime green": "#32CD32",
        "pale green": "#98FB98",
        "light green": "#90EE90",
        "medium spring green": "#00FA9A",
        "spring green": "#00FF7F",
        "medium sea green": "#3CB371",
        "sea green": "#2E8B57",
        "forest green": "#228B22",
        "green": "#008000",
        "dark green": "#006400",
        "yellow green": "#9ACD32",
        "olive drab": "#6B8E23",
        "olive": "#808000",
        "dark olive green": "#556B2F",
        "medium aquamarine": "#66CDAA",
        "dark sea green": "#8FBC8B",
        "light sea green": "#20B2AA",
        "dark cyan": "#008B8B",
        "teal": "#008080",
    }

    blue_color_dict = {
        "aqua": "#00FFFF",
        "cyan": "#00FFFF",
        "light cyan": "#E0FFFF",
        "pale turquoise": "#AFEEEE",
        "aquamarine": "#7FFFD4",
        "turquoise": "#40E0D0",
        "medium turquoise": "#48D1CC",
        "dark turquoise": "#00CED1",
        "cadet blue": "#5F9EA0",
        "steel blue": "#4682B4",
        "light steel blue": "#B0C4DE",
        "powder blue": "#B0E0E6",
        "light blue": "#ADD8E6",
        "sky blue": "#87CEEB",
        "light sky blue": "#87CEFA",
        "deep sky blue": "#00BFFF",
        "dodger blue": "#1E90FF",
        "cornflower blue": "#6495ED",
        "medium slate blue": "#7B68EE",
        "royal blue": "#4169E1",
        "blue": "#0000FF",
        "medium blue": "#0000CD",
        "dark blue": "#00008B",
        "navy": "#000080",
        "midnight blue": "#191970",
    }

    brown_color_dict = {
        "cornsilk": "#FFF8DC",
        "blanched almond": "#FFEBCD",
        "bisque": "#FFE4C4",
        "navajo white": "#FFDEAD",
        "wheat": "#F5DEB3",
        "burly wood": "#DEB887",
        "tan": "#D2B48C",
        "rosy brown": "#BC8F8F",
        "sandy brown": "#F4A460",
        "goldenrod": "#DAA520",
        "dark goldenrod": "#B8860B",
        "peru": "#CD853F",
        "chocolate": "#D2691E",
        "saddle brown": "#8B4513",
        "sienna": "#A0522D",
        "brown": "#A52A2A",
        "maroon": "#800000",
    }

    color_group = model.query(
        "which color strictly out of "
        + str(basic_colors).replace("[", "").replace("]", "").replace("'", "")
        + " is most suitable for "
        + prompt
        + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. ONLY PICK A COLOR FROM THE COLORS IN "
        + str(basic_colors).replace("[", "").replace("]", "").replace("'", "")
    )
    color_group = color_group.lower()

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
        recommended_bg_color = recommended_bg_color.lower()
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
        recommended_bg_color = recommended_bg_color.lower()
        if recommended_bg_color.lower() in green_color_dict.keys():
            hex_color = green_color_dict[recommended_bg_color]

    if color_group == "blue":
        recommended_bg_color = model.query(
            "which color out of "
            + str(blue_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        recommended_bg_color = recommended_bg_color.lower()
        if recommended_bg_color.lower() in blue_color_dict.keys():
            hex_color = blue_color_dict[recommended_bg_color]

    if color_group == "brown":
        recommended_bg_color = model.query(
            "which color out of "
            + str(brown_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        recommended_bg_color = recommended_bg_color.lower()
        if recommended_bg_color.lower() in brown_color_dict.keys():
            hex_color = brown_color_dict[recommended_bg_color]

    if color_group == "purple":
        recommended_bg_color = model.query(
            "which color out of "
            + str(purple_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        recommended_bg_color = recommended_bg_color.lower()
        if recommended_bg_color.lower() in purple_color_dict.keys():
            hex_color = purple_color_dict[recommended_bg_color]

    if color_group == "orange":
        recommended_bg_color = model.query(
            "which color out of "
            + str(orange_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        recommended_bg_color = recommended_bg_color.lower()
        if recommended_bg_color.lower() in orange_color_dict.keys():
            hex_color = orange_color_dict[recommended_bg_color]

    if color_group == "yellow":
        recommended_bg_color = model.query(
            "which color out of "
            + str(yellow_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        recommended_bg_color = recommended_bg_color.lower()
        if recommended_bg_color.lower() in yellow_color_dict.keys():
            hex_color = yellow_color_dict[recommended_bg_color]

    if color_group == "pink":
        recommended_bg_color = model.query(
            "which color out of "
            + str(pink_color_dict.keys())
            + " is most suitable for "
            + prompt
            + "YOU MUST ONLY RETURN THE COLOR MOST SUITED FOR THE BRAND, AND NO OTHER TEXT. DO NOT USE ANY COLOR WHICH IS NOT MENTIONED IN THE LIST"
        )
        recommended_bg_color = recommended_bg_color.lower()
        if recommended_bg_color.lower() in pink_color_dict.keys():
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

    recommended_fg_color = recommended_fg_color.lower()

    fg_hex_color = "#000000"

    if recommended_fg_color.lower() in red_color_dict.keys():
        fg_hex_color = red_color_dict[recommended_fg_color]

    if recommended_fg_color.lower() in pink_color_dict.keys():
        fg_hex_color = pink_color_dict[recommended_fg_color]

    if recommended_fg_color.lower() in orange_color_dict.keys():
        fg_hex_color = orange_color_dict[recommended_fg_color]

    if recommended_fg_color.lower() in yellow_color_dict.keys():
        fg_hex_color = yellow_color_dict[recommended_fg_color]

    if recommended_fg_color.lower() in green_color_dict.keys():
        fg_hex_color = green_color_dict[recommended_fg_color]

    if recommended_fg_color.lower() in blue_color_dict.keys():
        fg_hex_color = blue_color_dict[recommended_fg_color]

    if recommended_fg_color.lower() in brown_color_dict.keys():
        fg_hex_color = brown_color_dict[recommended_fg_color]

    if recommended_fg_color.lower() in purple_color_dict.keys():
        fg_hex_color = purple_color_dict[recommended_fg_color]

    # print(recommended_fg_color.lower())

    if hex_color == "default":
        print("default encountered", recommended_bg_color)

        # search through all of the dicts to find recommended_bg_color in keys, do an if elif ladder
        if recommended_bg_color in red_color_dict.keys():
            hex_color = red_color_dict[recommended_bg_color]
        elif recommended_bg_color in pink_color_dict.keys():
            hex_color = pink_color_dict[recommended_bg_color]
        elif recommended_bg_color in orange_color_dict.keys():
            hex_color = orange_color_dict[recommended_bg_color]
        elif recommended_bg_color in yellow_color_dict.keys():
            hex_color = yellow_color_dict[recommended_bg_color]
        elif recommended_bg_color in green_color_dict.keys():
            hex_color = green_color_dict[recommended_bg_color]
        elif recommended_bg_color in blue_color_dict.keys():
            hex_color = blue_color_dict[recommended_bg_color]
        elif recommended_bg_color in brown_color_dict.keys():
            hex_color = brown_color_dict[recommended_bg_color]
        elif recommended_bg_color in purple_color_dict.keys():
            hex_color = purple_color_dict[recommended_bg_color]

        if hex_color == "default":
            hex_color = "#000000"

    # print(recommended_bg_color)
    # print(str(hex_color))
    return (str(hex_color), str(fg_hex_color))
