import logging
import os

import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Text

from settings.config import (
    BotToken,
    SERVICES,
    GET_NEW_CODE,
    CANCEL_NUMBER,
    FINISH_NUMBER,
)
from smshub_api.api import SmsHubAPI
from telegram.keyboard import (
    main_keyboard_toggle,
    generate_services_keyboard,
    generate_status_keyboard,
)

bot = aiogram.Bot(token=BotToken, parse_mode=types.ParseMode.HTML)
dp = aiogram.Dispatcher(bot)
hub = SmsHubAPI()
logger = logging.getLogger(__name__)


async def check_user_id(message: aiogram.types.Message):
    """
    Check if the user is allowed to use the bot.
    :param message:
    :return:
    """
    if message.from_user.id != os.getenv('MY_CHAT_ID'):
        await message.answer('You are not allowed to use this bot')
        return False
    return True


@dp.message_handler(commands=['start'])
async def process_start_command(message: aiogram.types.Message):
    """
    Start command handler.
    Sends initial message and presents the user with the main keyboard.

    :param message: The received message.
    """
    if not await check_user_id(message):
        return
    await message.answer('🤖', reply_markup=main_keyboard_toggle)
    logging.info('Bot started')


@dp.message_handler(Text(equals=['💵 Balance']))
async def process_balance_command(message: aiogram.types.Message):
    """
    Balance command handler.
    Sends the current balance to the user.

    :param message: The received message.
    """
    if not await check_user_id(message):
        return
    await message.answer(await hub.get_balance())
    logger.info('Balance requested')


@dp.message_handler(Text(equals=['📞 Buy number']))
async def process_buy_number(message: aiogram.types.Message):
    """
    Buy number command handler.
    Sends services keyboard to the user.

    :param message: The received message.
    """
    if not await check_user_id(message):
        return
    services_keyboard = generate_services_keyboard()
    await message.answer('Choose service:', reply_markup=services_keyboard)
    logger.info('Num menu requested')


@dp.callback_query_handler(lambda c: c.data in SERVICES.values())
async def process_service_choice(callback_query: aiogram.types.CallbackQuery):
    """
    Service choice handler.
    Buys a number for the selected service and sends it to the user.
    Also sends status keyboard for further actions.

    :param callback_query: The received callback query.
    """
    if not await check_user_id(callback_query.message):
        return
    check_balance = float(await hub.get_balance())
    if check_balance <= 20.00:
        await bot.answer_callback_query(
            callback_query.id,
            text=f'Not enough money. Balance: {check_balance} RUB',
            show_alert=True,
        )
        logger.info('Not enough money')

    service_code = callback_query.data
    service_name = list(SERVICES.keys())[
        list(SERVICES.values()).index(service_code)
    ]
    await bot.answer_callback_query(callback_query.id)
    phone, phone_id = await hub.get_number(service_code)
    status_keyboard = generate_status_keyboard(phone_id, service_name, phone)
    sent_message = await bot.send_message(
        callback_query.from_user.id,
        text=f'{service_name}: <code>{phone}</code>',
        reply_markup=status_keyboard,
    )
    logger.info(f'Number {phone} bought')
    code = await hub.check_status(phone_id)
    if code == 'Номер закрыт':
        await bot.edit_message_text(
            text=f'{service_name}: <code>{phone}</code> | Number canceled',
            chat_id=sent_message.chat.id,
            message_id=sent_message.message_id,
            reply_markup=None,
        )
        logger.info(f'Number {phone} closed')
        return
    await bot.edit_message_text(
        text=f'{service_name}: <code>{phone}</code> | <code' f'>{code}</code>',
        chat_id=sent_message.chat.id,
        message_id=sent_message.message_id,
        reply_markup=status_keyboard,
    )
    logger.info(f'Code {code} received')


@dp.callback_query_handler(lambda c: c.data.startswith('cancel_'))
async def process_cancel_number(callback_query: aiogram.types.CallbackQuery):
    """
    Cancel number handler.
    Cancels the number by ID and sends a confirmation to the user.

    :param callback_query: The received callback query.
    """
    if not await check_user_id(callback_query.message):
        return
    number_id = callback_query.data.split('_')[1]
    await hub.set_status(number_id, CANCEL_NUMBER)
    await bot.answer_callback_query(
        callback_query.id, text='Number ' 'canceled'
    )
    logger.info(f'Number {number_id} canceled')
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=None,
    )


@dp.callback_query_handler(lambda c: c.data.startswith('get_'))
async def process_get_new_code(callback_query: aiogram.types.CallbackQuery):
    """
    Get new code handler.
    Requests a new code for the number and sends it to the user.

    :param callback_query: The received callback query.
    """
    if not await check_user_id(callback_query.message):
        return
    data = callback_query.data.split(';')
    number_id = data[0].split('_')[1]
    service_name = data[1]
    phone = data[2]

    await bot.answer_callback_query(
        callback_query.id, text='Waiting for new ' 'code'
    )
    await hub.set_status(number_id, GET_NEW_CODE)
    code = await hub.check_status(number_id)

    await bot.edit_message_text(
        text=f'{service_name}: '
             f'<code>{phone}</code> '
             f'|| '
             f'<code>{code}</code>',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=generate_status_keyboard(number_id, service_name, phone),
    )

    logger.info(f'New code {code} received')


@dp.callback_query_handler(lambda c: c.data.startswith('close_'))
async def process_close_after_sms(callback_query: aiogram.types.CallbackQuery):
    """
    Close number handler.
    Closes the number after the SMS and sends a confirmation to the user.

    :param callback_query: The received callback query.
    """
    if not await check_user_id(callback_query.message):
        return
    number_id = callback_query.data.split('_')[1]
    await hub.set_status(number_id, FINISH_NUMBER)
    await bot.answer_callback_query(callback_query.id, text='Finished')
    logger.info(f'Number {number_id} finished')
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=None,
    )
