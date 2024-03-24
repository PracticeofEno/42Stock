"""테스트"""
import asyncio
from classes.ksi_api import KsiApi

async def main():
    """
    a
    """
    ksi_api_client = KsiApi()
    await ksi_api_client.get_v_token()


if __name__ == '__main__':
    asyncio.run(main())
