from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)

from settings.config import SERVICES

main_keyboard_toggle = ReplyKeyboardMarkup(resize_keyboard=True)
numbers_keyboard_toggle = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard_toggle.add('💵 Balance', '📞 Buy number')


def generate_services_keyboard(page=0):
    """
    Generate an inline keyboard with buttons for each service.

    :param page: The page number to display. Defaults to 0.
    :return: InlineKeyboardMarkup object.
    """
    keyboard = InlineKeyboardMarkup()

    services = list(SERVICES.items())
    pages = [services[n: n + 6] for n in range(0, len(services), 6)]

    if page >= len(pages):
        return (
            keyboard  # Return an empty keyboard if the page number is too high
        )

    for service, code in pages[page]:
        button = InlineKeyboardButton(text=service, callback_data=code)
        keyboard.add(button)

    # Add navigation buttons if there are more than one page
    if len(pages) > 1:
        buttons = []
        if page > 0:
            buttons.append(
                InlineKeyboardButton(text='⬅️', callback_data=f'page:{page-1}')
            )
        if page < len(pages) - 1:
            buttons.append(
                InlineKeyboardButton(text='➡️', callback_data=f'page:{page+1}')
            )
        keyboard.row(*buttons)

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
