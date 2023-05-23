"""
The main script to run the bot.
"""

import logging

from aiogram import executor

from telegram.bot import dp

if __name__ == '__main__':
    # Set up logging configurations
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    # Start the bot
    executor.start_polling(dp, skip_updates=True)
