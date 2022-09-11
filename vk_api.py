import requests


VK_BASE_URL = "https://api.vk.com/method/"
VK_API_VERSION = "5.131"


def get_upload_url(vk_group_id: str, access_token: str):
    method = "photos.getWallUploadServer"
    payload = {
        "group_id": vk_group_id,
        "access_token": access_token,
        "v": VK_API_VERSION
    }
    response = requests.get(f"{VK_BASE_URL}{method}", params=payload)
    response.raise_for_status()
    upload_info = response.json()
    return upload_info["response"].get("upload_url")


def upload_image_to_vk_server(filepath: str, server_url: str) -> dict:
    with open(filepath, "rb") as file:
        url = server_url
        payload = {
            "photo": file
        }
        response = requests.post(url, files=payload)
        response.raise_for_status()
    result = response.json()

    return {
        "photo": result.get("photo"),
        "server": result.get("server"),
        "hash": result.get("hash")
    }


def save_image_to_vk_album(
        vk_group_id: str,
        access_token: str,
        upload_info: dict
        ):
    method = "photos.saveWallPhoto"
    payload = {
        "photo": upload_info.get("photo"),
        "server": upload_info.get("server"),
        "hash": upload_info.get("hash"),
        "group_id": vk_group_id,
        "access_token": access_token,
        "v": VK_API_VERSION
    }
    response = requests.post(f"{VK_BASE_URL}{method}", params=payload)
    response.raise_for_status()
    result_info = response.json()
    owner_id = result_info["response"][0].get("owner_id")
    image_id = result_info["response"][0].get("id")
    return (owner_id, image_id)


def publish_post(
        access_token: str,
        vk_group_id: int,
        image_filepath: str,
        commentary: str
        ) -> None:
    server_url = get_upload_url(vk_group_id, access_token)
    upload_info = upload_image_to_vk_server(image_filepath, server_url)
    owner_id, image_id = save_image_to_vk_album(
        vk_group_id,
        access_token,
        upload_info
    )
    method = "wall.post"
    payload = {
        "owner_id": f"-{vk_group_id}",
        "from_group": 1,
        "message": commentary,
        "attachments": f"photo{owner_id}_{image_id}",
        "access_token": access_token,
        "v": VK_API_VERSION
    }
    response = requests.post(f"{VK_BASE_URL}{method}", params=payload)
    response.raise_for_status()
