"""테스트"""
import asyncio
from classes.ksi_api import KsiApi

async def main():
    """
    a
    """
    jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjQxY2QxN2VlLTBiNjItNDdiMy1iMmVmLTE0ODJhMTFiOWVjMSIsImlzcyI6InVub2d3IiwiZXhwIjoxNzExMzgwNTMwLCJpYXQiOjE3MTEyOTQxMzAsImp0aSI6IlBTeklrNTR4ZGNoakJyU21rczhVMWYwam5mVzRBdzZYU0pxNCJ9.az3guQ38vv-6L3iQgJHBhD0cwqKyrgJH-eyirAF0eHamvuzWBycfk1dOSnulYjntyfinlBUhCUjG-orcMf6VfA"
    ksi_api_client = KsiApi(jwt)
    await ksi_api_client.set_credentails()
    # await ksi_api_client.get_v_token()


if __name__ == '__main__':
    asyncio.run(main())
