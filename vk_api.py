import requests


VK_BASE_URL = "https://api.vk.com/method/"


def get_upload_url(vk_group_id: str, access_token: str, vk_api_version: str):
    method = "photos.getWallUploadServer"
    payload = {
        "group_id": vk_group_id,
        "access_token": access_token,
        "v": vk_api_version
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
        return {
            "photo": response.json().get("photo"),
            "server": response.json().get("server"),
            "hash": response.json().get("hash")
        }


def save_image_to_vk_album(
        vk_group_id: str,
        access_token: str,
        vk_api_version: str,
        upload_info: dict
        ):
    method = "photos.saveWallPhoto"
    payload = {
        "photo": upload_info.get("photo"),
        "server": upload_info.get("server"),
        "hash": upload_info.get("hash"),
        "group_id": vk_group_id,
        "access_token": access_token,
        "v": vk_api_version
    }
    response = requests.post(f"{VK_BASE_URL}{method}", params=payload)
    response.raise_for_status()
    result_info = response.json()
    return {
        "owner_id": result_info["response"][0].get("owner_id"),
        "image_id": result_info["response"][0].get("id")
    }


def publish_post(
        access_token: str,
        vk_api_version: str,
        vk_group_id: int,
        comics_info: dict
        ) -> None:
    server_url = get_upload_url(vk_group_id, access_token, vk_api_version)
    filepath = comics_info.get("downloaded_image")
    upload_info = upload_image_to_vk_server(filepath, server_url)
    saved_image_info = save_image_to_vk_album(
        vk_group_id,
        access_token,
        vk_api_version,
        upload_info
    )
    message = comics_info.get("comics_commentary")
    owner_id = saved_image_info.get("owner_id")
    image_id = saved_image_info.get("image_id")
    method = "wall.post"
    payload = {
        "owner_id": f"-{vk_group_id}",
        "from_group": 1,
        "message": message,
        "attachments": f"photo{owner_id}_{image_id}",
        "access_token": access_token,
        "v": vk_api_version
    }
    response = requests.post(f"{VK_BASE_URL}{method}", params=payload)
    response.raise_for_status()
