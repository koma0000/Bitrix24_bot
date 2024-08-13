import asyncio

import requests
import aiohttp
from aiohttp import TCPConnector
from urllib.parse import unquote
from io import BytesIO

class BitrixAPIException(Exception):
    pass

class Bitrix:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def get_file_url(self, deal_id: int):
        api_method = 'crm.item.get'
        params = {
            'entityTypeId': 1036,
            'id': deal_id
        }

        response = requests.get(f'{self.webhook_url}/{api_method}', params=params)

        if response.status_code != 200:
            raise BitrixAPIException(f"Failed to fetch item data from Bitrix, status code: {response.status_code}")

        data = response.json()
        file_url = data.get('result', {}).get('item', {}).get('ufCrm5_1723557005675', {}).get('urlMachine')
        return file_url if file_url else None

    async def _download_file_async(self, file_url: str):
        connector = TCPConnector(ssl=False)

        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    content_disposition = response.headers.get('Content-Disposition')
                    if content_disposition:
                        filename = content_disposition.split('filename=')[1].strip('"\'')
                        filename = unquote(filename)
                    else:
                        filename = 'downloaded_file'

                    file_content = await response.read()
                    file = BytesIO(file_content)
                    file.name = filename

                    print(f"Файл успешно скачан и сохранен в памяти как {filename}")
                    return file
                else:
                    raise BitrixAPIException(f"Failed to download file, status code: {response.status}")

    def download_file(self, file_url: str):
        return asyncio.run(self._download_file_async(file_url))
