import requests
from config import base_url

login_url = f"{base_url}/api/auth/login/"


def login(username, password):
    login_data = {
        "username": username,
        "password": password
    }

    response = requests.post(
        url=login_url,
        json=login_data
    )

    return response
    
def get_equipment(access_token):
    equipment_url = f"{base_url}/api/equipment/instances/"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        equipment_url,
        headers=headers
    )

    return response