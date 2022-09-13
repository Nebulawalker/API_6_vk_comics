import requests


VK_BASE_URL = "https://api.vk.com/method/"
VK_API_VERSION = "5.131"


def get_upload_url(vk_group_id: str, vk_access_token: str):
    method = "photos.getWallUploadServer"
    payload = {
        "group_id": vk_group_id,
        "access_token": vk_access_token,
        "v": VK_API_VERSION
    }
    response = requests.get(f"{VK_BASE_URL}{method}", params=payload)
    response.raise_for_status()
    upload_info = response.json()
    return upload_info["response"]["upload_url"]


def upload_image_to_vk_server(filepath: str, server_url: str) -> dict:
    with open(filepath, "rb") as file:
        url = server_url
        payload = {
            "photo": file
        }
        response = requests.post(url, files=payload)
        response.raise_for_status()
    uploaded_image_params = response.json()
    photo = uploaded_image_params["photo"]
    server = uploaded_image_params["server"]
    image_hash = uploaded_image_params["hash"]

    return photo, server, image_hash


def save_image_to_vk_album(
        vk_group_id: str,
        vk_access_token: str,
        photo: str,
        server: str,
        image_hash: str
        ):
    method = "photos.saveWallPhoto"
    payload = {
        "photo": photo,
        "server": server,
        "hash": image_hash,
        "group_id": vk_group_id,
        "access_token": vk_access_token,
        "v": VK_API_VERSION
    }
    response = requests.post(f"{VK_BASE_URL}{method}", params=payload)
    response.raise_for_status()
    saved_image_params = response.json()
    owner_id = saved_image_params["response"][0]["owner_id"]
    image_id = saved_image_params["response"][0]["id"]
    return owner_id, image_id


def publish_post(
        vk_access_token: str,
        vk_group_id: int,
        image_filepath: str,
        commentary: str
        ) -> None:
    server_url = get_upload_url(vk_group_id, vk_access_token)
    photo, server, image_hash = upload_image_to_vk_server(
        image_filepath, server_url
        )
    owner_id, image_id = save_image_to_vk_album(
        vk_group_id,
        vk_access_token,
        photo,
        server,
        image_hash
    )
    method = "wall.post"
    payload = {
        "owner_id": f"-{vk_group_id}",
        "from_group": 1,
        "message": commentary,
        "attachments": f"photo{owner_id}_{image_id}",
        "access_token": vk_access_token,
        "v": VK_API_VERSION
    }
    response = requests.post(f"{VK_BASE_URL}{method}", params=payload)
    response.raise_for_status()
