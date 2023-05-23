import json
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# SmsHub API key (obtained from https://smshub.org/)
APIKEY = os.getenv('SMSHUB_API')
# Main URL for SmsHub API requests
MAIN_URL = f'https://smshub.org/stubs/handler_api.php?api_key={APIKEY}&action='

# Constants for setting status
CANCEL_NUMBER = 8
GET_NEW_CODE = 3
FINISH_NUMBER = 6

# Load the dictionary of services and their corresponding codes
# from an environment variable
SERVICES = json.loads(os.getenv('SERVICES_DICT'))

"""
Example of the structure of the services dictionary:

SERVICES_DICT = {
    'Service name': 'Service code',
"""

# Telegram bot token (obtained from https://core.telegram.org/bots/api)
BotToken = os.getenv('BOT_TOKEN')
