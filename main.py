import logging

from aiogram import executor

from telegram.bot import dp

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    executor.start_polling(dp, skip_updates=True)
