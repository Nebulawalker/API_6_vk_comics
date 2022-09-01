import os
import requests

from typing import Iterable
from urllib.parse import urlparse


def download_images(
    urls: Iterable,
    service: str,
    payload: dict | None = None
) -> None:
    os.chdir(os.path.dirname(__file__))
    os.makedirs("image", exist_ok=True)
    for index, url in enumerate(urls):
        response = requests.get(url, params=payload)
        response.raise_for_status()
        file_extension = get_extension(url)
        path = os.path.join(
            "image",
            f"{service}_{index}{file_extension}"
        )
        with open(path, "wb") as file:
            file.write(response.content)
    return path


def get_extension(url):
    parsed_url = urlparse(url)
    file_path = os.path.splitext(parsed_url.path)
    file_extension = file_path[1]
    return file_extension
