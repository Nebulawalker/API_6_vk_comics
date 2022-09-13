import os
from dotenv import load_dotenv

from vk_api import publish_post
from xkcd_api import get_random_xkcd_comic


def main():
    load_dotenv()
    vk_access_token = os.getenv("VK_ACCESS_TOKEN")
    vk_group_id = os.getenv("VK_GROUP_ID")
    try:
        image_filepath, comic_commentary = get_random_xkcd_comic()

        publish_post(
            vk_access_token,
            vk_group_id,
            image_filepath,
            comic_commentary
        )

    finally:
        os.remove(image_filepath)


if __name__ == "__main__":
    main()
