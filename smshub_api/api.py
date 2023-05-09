import asyncio
import logging
import httpx

from settings.config import MAIN_URL


class SmsHubAPI:
    def __init__(self):
        self.main_url = MAIN_URL

    async def get_balance(self):
        url = f'{self.main_url}getBalance'
        try:
            response = await httpx.AsyncClient().get(url)
            logging.info(f'Balance requested: {response.text}')
            return response.text[15:]
        except Exception as e:
            logging.error(e)
            return e

    async def get_number(self, service, country=0):
        url = f'{self.main_url}getNumber&service={service}&country={country}'
        try:
            response = await httpx.AsyncClient().get(url)
            logging.info(f'Number requested: {response.text}')
            if response.text == 'NO_NUMBERS':
                return 'Numbers are over'
            elif response.text == 'NO_BALANCE':
                return 'Not enough money'
            number_id = response.text[14:23]
            number = response.text[25:36]
            return number, number_id
        except Exception as e:
            logging.error(e)
            return e

    async def request_status(self, number_id):
        url = f'{self.main_url}getStatus&id={number_id}'
        try:
            response = await httpx.AsyncClient().get(url)
            logging.info(f'Status requested:{number_id} - {response.text}')
            return response.text
        except Exception as e:
            logging.error(e)
            return e

    async def check_status(self, number_id):
        try:
            for check in range(600):
                status = await self.request_status(number_id)
                logging.info(f'Checking status: {status}')
                await asyncio.sleep(5)
                if status == 'STATUS_WAIT_CODE':
                    continue
                elif status.split(':')[0] == 'STATUS_OK':
                    return status[10:]
                elif status == 'STATUS_CANCEL':
                    return 'Номер закрыт'
        except Exception as e:
            logging.error(e)
            return e

    async def set_status(self, number_id, status):
        url = f'{self.main_url}setStatus&status={status}&id={number_id}'
        try:
            response = await httpx.AsyncClient().get(url)
            logging.info(f'Status set: {response.text}')
            return response.text
        except Exception as e:
            logging.error(e)
            return e
