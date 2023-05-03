import json
import os
from dotenv import load_dotenv

load_dotenv()

# SmsHub API: https://smshub.org/
APIKEY = os.getenv('SMSHUB_API')
MAIN_URL = f'https://smshub.org/stubs/handler_api.php?api_key={APIKEY}&action='
# Codes for setting status
CANCEL_NUMBER = 8
GET_NEW_CODE = 3
FINISH_NUMBER = 6
# Dictionary of services and their codes
SERVICES = json.loads(os.getenv('SERVICES_DICT'))
"""
# Example of services dictionary
SERVICES_DICT = {
    'Service name': 'Service code',
"""
# Telegram bot API: https://core.telegram.org/bots/api
BotToken = os.getenv('BOT_TOKEN')
