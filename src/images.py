import time
import requests
import json
import asyncio


async def getImages(info):
    # for i in info:
    #     print(i["image"])

    img_url_list = []
    for i in info:
        # using a custom api https://edcomposer.vercel.app/api/getGoogleResult?search={i['image']} for image search
        max_retries = 3  # specify the maximum number of retries if the request fails
        current_retry = 0

        while current_retry < max_retries:
            try:
                response = requests.get(
                    f"https://edcomposer.vercel.app/api/getGoogleResult?search={i['image']}%20powerpoint%20presentation%20clipart%20style."
                )
                img_url_list.append(response.json()[0])
                break  # exit the loop if the request is successful
            except Exception:
                current_retry += 1
                print(f"Retrying in 1 second... (attempt {current_retry}/{max_retries})")
                time.sleep(1)

        if current_retry == max_retries:
            print(f"Failed to retrieve image after {max_retries} attempts. Skipping this image.")
            continue

        time.sleep(1)

    return img_url_list


async def main():
    with open("sample.json", "r") as f:
        answer = json.load(f)
    result = await getImages(answer)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
