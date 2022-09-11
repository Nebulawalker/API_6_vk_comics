import os
import requests


def download_image(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    path = os.path.basename(url)
    with open(path, "wb") as file:
        file.write(response.content)
    return path
