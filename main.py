import requests
import time
from datetime import datetime
from params import PARAMS  # Import the parameters from params.py
from cred import TELEGRAM_API_TOKEN,CHAT_ID,BASE_URL

# Track sent earthquakes
sent_earthquakes = set()

# Function to send a Telegram message
def send_telegram_message(message, photo_path=None):
    if photo_path:
        # Send photo with caption
        url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendPhoto"
        with open(photo_path, "rb") as photo:
            payload = {"chat_id": CHAT_ID, "caption": message, "parse_mode": "HTML"}
            files = {"photo": photo}
            response = requests.post(url, data=payload, files=files)
    else:
        # Send text-only message
        url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        response = requests.post(url, data=payload)
    response.raise_for_status()

# Function to determine earthquake severity
def get_severity_level(magnitude):
    if magnitude < 4.0:
        return "Minor 🌱"
    elif 4.0 <= magnitude < 5.0:
        return "Light 🌟"
    elif 5.0 <= magnitude < 6.0:
        return "Moderate ⚠️"
    elif 6.0 <= magnitude < 7.0:
        return "Strong 🚨"
    elif 7.0 <= magnitude < 8.0:
        return "Major 🔥"
    else:
        return "Great 💥"

# Function to fetch earthquake data
def get_earthquake():
    response = requests.get(BASE_URL, params=PARAMS)
    response.raise_for_status()
    return response.json()

# Main loop to monitor earthquakes
while True:
    try:
        data = get_earthquake()
        if data:
            for earthquake in data["features"]:
                earthquake_id = earthquake["id"]  # Unique ID for the earthquake
                if earthquake_id not in sent_earthquakes:
                    properties = earthquake["properties"]
                    mag = properties["mag"]
                    place = properties["place"]
                    time_epoch = properties["time"]

                    # Convert epoch time to human-readable format
                    time_str = datetime.utcfromtimestamp(time_epoch / 1000).strftime('%Y-%m-%d %H:%M:%S')

                    # Get severity level
                    severity = get_severity_level(mag)

                    # Construct the message
                    message = (
                        f"<b>🌍 New Earthquake Alert!</b>\n"
                        f"<b>Magnitude:</b> {mag} ({severity})\n"
                        f"<b>Location:</b> {place}\n"
                        f"<b>Time:</b> {time_str}\n"
                    )

                    # Path to the banner image
                    banner_image = "earthquake.jpeg"

                    # Send the message with the banner image and track the earthquake
                    send_telegram_message(message, photo_path=banner_image)
                    print(f"Message sent with banner: {message}")
                    sent_earthquakes.add(earthquake_id)

    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    time.sleep(10)  # Wait 10 seconds before checking again
