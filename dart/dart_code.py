"""다트의 고유번호 가져오는 파이썬 파일"""
import asyncio
import os
import sys
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from classes import stcok_db, ksi_api # pylint: disable=C0413

def download_dart_code(base: str):
    """코스피 종목 리스트 리턴"""
    dart_api_key = os.getenv('DART_API_KEY')
    print(dart_api_key)
    url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={dart_api_key}"
    urllib.request.urlretrieve(url, base + "/dart/dart_code.zip")

    os.chdir(base + "/dart")
    kospi_zip = zipfile.ZipFile('dart_code.zip')
    kospi_zip.extractall()

    kospi_zip.close()

    if os.path.exists("dart_code.zip"):
        os.remove("dart_code.zip")

async def stock_code_update(base: str, stock_db: stcok_db.StockDB, ksi_api_client: ksi_api.KsiApi):
    """매일 8시 30분에 실행되는 종목코드 업데이트"""
    await stock_db.delete_stock_table()
    tree = ET.parse(f"{base}/dart/CORPCODE.xml")
    root = tree.getroot()
    count = 0
    # 'corp_code', 'corp_name' 등의 요소를 가져오고 출력합니다.
    for list_element in root.findall('.//list'):
        corp_code = list_element.find('corp_code').text
        corp_name = list_element.find('corp_name').text
        stock_code = list_element.find('stock_code').text
        modify_date = list_element.find('modify_date').text
        if stock_code == ' ':
            continue
        try:
            await stock_db.create_stock(corp_name, stock_code, corp_code)
            print("corp_code:", corp_code)
            print("corp_name:", corp_name)
            print("stock_code:", stock_code)
            print("modify_date:", modify_date)
        except: # pylint: disable=W0702
            pass
        count += 1
    print(count)

async def main():
    """진입점""" 
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6Ijk4ZjQ4MjBmLTJkMjItNDlhNS1hMDhjLTNlYzM5YTQ3ZjE1NiIsImlzcyI6InVub2d3IiwiZXhwIjoxNzExNTA4MTI1LCJpYXQiOjE3MTE0MjE3MjUsImp0aSI6IlBTeklrNTR4ZGNoakJyU21rczhVMWYwam5mVzRBdzZYU0pxNCJ9.Iu83s49vC7gAbEkUZHD209P3MdvK80SSehxt5M-7YUNRr312nNhYR1UIKWZnE-BjvqsIYSkZ1pZeP8gAm5F0yQ" # pylint: disable=C0301
    ksi_api_client = ksi_api.KsiApi(access_token=access_token)
    await ksi_api_client.set_credentails()
    stock_db = stcok_db.StockDB()
    await stock_db.connect()
    base_dir = os.getcwd()
    download_dart_code(base_dir)
    await stock_code_update(base_dir, stock_db, ksi_api_client)

if __name__ == '__main__':
    asyncio.run(main())
