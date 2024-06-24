import requests
import json
import asyncio


async def getImages(info):
    # for i in info:
    #     print(i["image"])

    img_url_list = []
    for i in info:
        # using a custom api https://edcomposer.vercel.app/api/getGoogleResult?search={i['image']} for image search
        response = requests.get(
            f"https://edcomposer.vercel.app/api/getGoogleResult?search={i['image']}. powerpoint presentation clipart style."
        )
        img_url_list.append(response.json()[0])

    return img_url_list


async def main():
    with open("sample.json", "r") as f:
        answer = json.load(f)
    result = await getImages(answer)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
