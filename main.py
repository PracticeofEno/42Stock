"""테스트"""
import asyncio
import os
from datetime import datetime
from classes.ksi_api import KsiApi
from dart.dart_api import DartApi

async def main():
    """
    a
    """
    # access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6Ijk4ZjQ4MjBmLTJkMjItNDlhNS1hMDhjLTNlYzM5YTQ3ZjE1NiIsImlzcyI6InVub2d3IiwiZXhwIjoxNzExNTA4MTI1LCJpYXQiOjE3MTE0MjE3MjUsImp0aSI6IlBTeklrNTR4ZGNoakJyU21rczhVMWYwam5mVzRBdzZYU0pxNCJ9.Iu83s49vC7gAbEkUZHD209P3MdvK80SSehxt5M-7YUNRr312nNhYR1UIKWZnE-BjvqsIYSkZ1pZeP8gAm5F0yQ" # pylint: disable=C0301
    # ksi_api_client = KsiApi(access_token)
    # await ksi_api_client.set_credentails()
    # result = await ksi_api_client.check_delisting("036720")
    # print(result)
    
    dart_api_client = DartApi()
    await dart_api_client.db_connect()
    today = datetime.today().strftime('%Y%m%d')
    response = await dart_api_client.search_disclosure("20240403")
    print(response)
if __name__ == '__main__':
    asyncio.run(main())
