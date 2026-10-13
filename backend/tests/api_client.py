import logging
import requests

from config import base_url, DEFAULT_TIMEOUT

logger = logging.getLogger(__name__)

login_url = f"{base_url}/api/auth/login/"

equipment_url = f"{base_url}/api/equipment/instances/"

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
        json=login_data,
        timeout=DEFAULT_TIMEOUT
    )

    return response
    
def get_equipment(access_token=None, session=None, params=None):

    logger.info(
        "Sending GET request to %s",
        equipment_url
    )

    try:
        if session is not None:
            response = session.get(
                equipment_url,
                params=params,
                timeout=DEFAULT_TIMEOUT
            )
        else:
            response = requests.get(
                equipment_url,
                headers=build_headers(access_token),
                params=params,
                timeout=DEFAULT_TIMEOUT
            )

    except requests.exceptions.Timeout:
        logger.error("Equipment API request timed out")
        raise

    except requests.exceptions.ConnectionError:
        logger.error("Equipment API connection failed")
        raise

    logger.info(
        "Equipment API returned status code: %s",
        response.status_code
    )

    return response

def get_equipment_types(access_token):
    equipment_types_url = f"{base_url}/api/equipment/types/"

    response = requests.get(
        equipment_types_url,
        headers=build_headers(access_token),
        timeout=DEFAULT_TIMEOUT
    )

    return response

def create_equipment(access_token, equipment_data):
    url = equipment_url

    response = requests.post(
        url,
        headers=build_headers(access_token),
        json=equipment_data,
        timeout=DEFAULT_TIMEOUT
    )

    return response
    

def delete_equipment(access_token, equipment_id):
    url = f"{equipment_url}{equipment_id}/"

    response = requests.delete(
        url,
        headers=build_headers(access_token),
        timeout=DEFAULT_TIMEOUT
    )

    return response
    

def get_equipment_by_id(access_token, equipment_id):
    url = f"{equipment_url}{equipment_id}/"

    return requests.get(
        url,
        headers=build_headers(access_token),
        timeout=DEFAULT_TIMEOUT
    )