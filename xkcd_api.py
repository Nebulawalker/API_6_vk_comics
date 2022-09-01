import requests
from random import randint

from filesystem_helpers import download_images


XKCD_BASE_URL = "https://xkcd.com/"


def get_random_xkcd_comics() -> str:
    url = f"{XKCD_BASE_URL}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comics_release = randint(1, response.json().get("num"))
    url = f"{XKCD_BASE_URL}{str(comics_release)}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    record = response.json()
    image_link = record.get("img")
    comics_commentary = record.get("alt")
    filepath = download_images((image_link,), "XKCD-comics")
    return {
        "downloaded_image": filepath,
        "comics_commentary": comics_commentary
    }
