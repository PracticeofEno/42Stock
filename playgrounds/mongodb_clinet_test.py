"""몽고디비 관련 클라이언트 테스트 파일"""
import asyncio
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from dart.dart_api import DartApi # pylint: disable=C0413

load_dotenv()

async def main():
    """
    테스트
    """
    dart_api_client = DartApi()
    await dart_api_client.db_connect()
    response = await dart_api_client.search_disclosure("20240403")
    print(response)
    await dart_api_client.download_origin_disclosure("20190401004781")
if __name__ == '__main__':
    asyncio.run(main())
