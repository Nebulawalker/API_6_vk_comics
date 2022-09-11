import os
from dotenv import load_dotenv

from vk_api import publish_post
from xkcd_api import get_random_xkcd_comics


def main():
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")
    vk_group_id = os.getenv("VK_GROUP_ID")
    comics_info = get_random_xkcd_comics()
    publish_post(access_token, vk_group_id, comics_info)
    os.remove(comics_info.get("downloaded_image"))


if __name__ == "__main__":
    main()
