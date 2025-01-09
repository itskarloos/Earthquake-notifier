import requests
from datetime import datetime
from params import PARAMS  # Import the parameters from params.py
from cred import TELEGRAM_API_TOKEN, BASE_URL
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext


# Initialize the bot
bot = Bot(token=TELEGRAM_API_TOKEN)

# Track sent earthquakes
sent_earthquakes = set()

# Store chat_id for use in main loop
chat_id = None

# Function to send a Telegram message
async def send_telegram_message(chat_id, message, photo_path=None):
    try:
        if photo_path:
            # Send photo with caption
            with open(photo_path, 'rb') as photo:
                await bot.send_photo(chat_id=chat_id, photo=photo, caption=message, parse_mode='HTML')
        else:
            # Send text-only message
            await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
    except Exception as e:
        print(f"Error sending message: {e}")

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
    try:
        response = requests.get(BASE_URL, params=PARAMS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching earthquake data: {e}")
        return None

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    global chat_id
    chat_id = update.message.chat_id
    start_message = (
        "<b>🌍 Welcome to the Ethiopia Earthquake Alert Bot 🇪🇹!</b>\n\n"
        "This bot provides real-time updates about earthquakes in Ethiopia, "
        "including their magnitude, location, time, and severity level.\n\n"
        "Stay safe and informed!"
    )
    banner_image = "earthquake.jpeg"  # Path to the welcome banner
    await send_telegram_message(chat_id, start_message, photo_path=banner_image)

# Function to check and send earthquake alerts
async def check_earthquake(context: CallbackContext):
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
                if chat_id:
                    await send_telegram_message(chat_id=chat_id, message=message, photo_path=banner_image)
                    print(f"Message sent with banner: {message}")
                    sent_earthquakes.add(earthquake_id)

# Main function to initialize the bot
def main():
    # Initialize the Application with the token
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Add handler for /start command
    application.add_handler(CommandHandler('start', start))

    # Initialize JobQueue and schedule earthquake checking every 10 seconds
    job_queue = application.job_queue  # Access job_queue from application object
    job_queue.run_repeating(check_earthquake, interval=10, first=0)  # Check every 10 seconds

    # Start polling
    application.run_polling()

if __name__ == '__main__':
    # Directly run the bot without asyncio
    main()
