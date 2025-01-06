import requests
from params import PARAMS  # Import parameters from params.py
import time

# Base URL for the API
BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Make the request
def get_earthquake():
    response = requests.get(BASE_URL, params=PARAMS)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    data = response.json()
    return data

while True:
    data = get_earthquake()
    if data:
        print(f"Number of earthquakes: {len(data['features'])}")
        for earthquake in data["features"]:
            properties = earthquake["properties"]
            print(f"Magnitude: {properties['mag']}, Location: {properties['place']}, Time: {properties['time']}")
    time.sleep(10)
