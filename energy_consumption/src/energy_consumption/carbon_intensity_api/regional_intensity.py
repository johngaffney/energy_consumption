import json
import requests

from ..constants import CARBON_INTENSITY_API


def get_regional_intensity_by_postcode(start_time: str, end_time: str, postcode: str):
    headers = {"Accept": "application/json"}
    base_url = CARBON_INTENSITY_API
    query_string = f"{start_time}/{end_time}/postcode/{postcode}"
    url = f"{base_url}regional/intensity/{query_string}"
    response = requests.get(url, params={}, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Error getting regional intensity by postcode: {response.status_code}")
