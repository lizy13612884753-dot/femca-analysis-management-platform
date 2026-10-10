import requests
from config import base_url

login_url = f"{base_url}/api/auth/login/"

def build_headers(access_token=None):
    headers = {}

    if access_token is not None:
        headers["Authorization"] = f"Bearer {access_token}"

    return headers

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
    
def get_equipment(access_token=None, session=None):
    equipment_url = f"{base_url}/api/equipment/instances/"

    if session is not None:
        response = session.get(equipment_url)
    else:
        response = requests.get(
            equipment_url,
            headers=build_headers(access_token)
        )

    return response

def get_equipment_types(access_token):
    equipment_url = f"{base_url}/api/equipment/types/"

    response = requests.get(
        equipment_url,
        headers=build_headers(access_token)
    )

    return response

def create_equipment(access_token, equipment_data):
    url = f"{base_url}/api/equipment/instances/"

    response = requests.post(
        url,
        headers=build_headers(access_token),
        json=equipment_data
    )

    return response
    

def delete_equipment(access_token, equipment_id):
    url = f"{base_url}/api/equipment/instances/{equipment_id}/"

    response = requests.delete(
        url,
        headers=build_headers(access_token)
    )

    return response
    

def get_equipment_by_id(access_token, equipment_id):
    url = f"{base_url}/api/equipment/instances/{equipment_id}/"

    return requests.get(
        url,
        headers=build_headers(access_token)
    )