import requests
from ..constants import OPEN_VOLT_API_KEY, OPEN_VOLT_API


def retrieve_customer(customer_id: str, api_key: str = OPEN_VOLT_API_KEY):
    base_url = OPEN_VOLT_API
    url = f"{base_url}/customers/{customer_id}"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error retrieving customer: {response.status_code}")
