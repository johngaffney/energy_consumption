import requests
from ..constants import OPEN_VOLT_API_KEY, OPEN_VOLT_API
import json


def get_interval_data(
    meter_id: str,
    start_date: str,
    end_date: str,
    granularity: str,
    api_key: str = OPEN_VOLT_API_KEY,
):
    base_url = OPEN_VOLT_API
    query_string = f"meter_id={meter_id}&granularity={granularity}&start_date={start_date}&end_date={end_date}"
    url = f"{base_url}interval-data?{query_string}"
    headers = {"accept": "application/json", "x-api-key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Error retrieving interval data: {response.status_code}")
