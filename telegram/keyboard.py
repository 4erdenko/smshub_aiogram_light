from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup

from settings.config import SERVICES

main_keyboard_toggle = ReplyKeyboardMarkup(resize_keyboard=True)
numbers_keyboard_toggle = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard_toggle.add('💵 Balance', '📞 Buy number')


def generate_services_keyboard():
    """
    Generate an inline keyboard with buttons for each service.

    :return: InlineKeyboardMarkup object.
    """
    keyboard = InlineKeyboardMarkup()
    for service, code in SERVICES.items():
        button = InlineKeyboardButton(text=service, callback_data=code)
        keyboard.add(button)
    return keyboard


def generate_status_keyboard(number_id, service_name, phone):
    """
    Generate an inline keyboard with buttons for number actions
    (cancel, get new code, finish).

    :param number_id: Id of the number to be manipulated.
    :param service_name: Name of the service the number is used for.
    :param phone: Phone number as a string.
    :return: InlineKeyboardMarkup object.
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Cancel', callback_data=f'cancel_{number_id}'
        ),
        InlineKeyboardButton(
            text='Get new code',
            callback_data=f'get_{number_id};{service_name};{phone}',
        ),
        InlineKeyboardButton(
            text='Finish', callback_data=f'close_{number_id}'
        ),
    )
    return keyboard
