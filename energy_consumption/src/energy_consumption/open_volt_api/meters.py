import requests
from ..constants import OPEN_VOLT_API_KEY, OPEN_VOLT_API
import json


def retrieve_meter(meter_id: str, api_key: str = OPEN_VOLT_API_KEY):
    base_url = OPEN_VOLT_API
    url = f"{base_url}meters/{meter_id}"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Error retrieving meter: {response.status_code}")
