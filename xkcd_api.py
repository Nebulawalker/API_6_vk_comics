import requests
import os
from random import randint


XKCD_BASE_URL = "https://xkcd.com/"


def get_random_xkcd_comic() -> str:
    url = f"{XKCD_BASE_URL}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comics_release = randint(1, response.json().get("num"))
    url = f"{XKCD_BASE_URL}{str(comics_release)}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    record = response.json()

    image_link = record.get("img")
    response = requests.get(image_link)
    response.raise_for_status()
    filepath = os.path.basename(image_link)
    with open(filepath, "wb") as file:
        file.write(response.content)

    comic_commentary = record.get("alt")
    return (filepath, comic_commentary)
