"""dart_code와 유사하지만 dart_code는 매일 실행되면서 유지보수, first_init은 DB밀고 다시 씀"""
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
    """
    매일 8시 30분에 실행되는 종목코드 업데이트
    """
    # stock 테이블 초기화
    await stock_db.delete_stock_table()
    tree = ET.parse(f"{base}/dart/CORPCODE.xml")
    root = tree.getroot()
    count = 0
    parsed_list = []
    # 'corp_code', 'corp_name' 등의 요소를 가져오고 출력합니다.
    for list_element in root.findall('.//list'):
        corp_code = list_element.find('corp_code').text
        corp_name = list_element.find('corp_name').text
        stock_code = list_element.find('stock_code').text
        modify_date = list_element.find('modify_date').text
        if stock_code == ' ':
            continue
        parsed_list.append({
            'corp_code': corp_code,
            'corp_name': corp_name,
            'stock_code': stock_code,
            'modify_date': modify_date
        })
    print(len(parsed_list))

    while len(parsed_list) > 0:
        stock = parsed_list[0]
        try:
            is_delisted = await ksi_api_client.check_delisting(stock['stock_code'])
            if is_delisted:
                print(f"{stock['corp_name']} is delisted")
                parsed_list.remove(stock)
                continue
            await stock_db.create_stock(stock['corp_name'], stock['stock_code'], stock['corp_code'])
            print("corp_code:", stock['corp_code'])
            print("corp_name:", stock['corp_name'])
            print("stock_code:", stock['stock_code'])
            print("modify_date:", stock['modify_date'])
            parsed_list.remove(stock)
        except Exception as e: # pylint: disable=W0702 W0718
            print(e)
            print(f"Error: {stock['corp_name']} wait 5 seconds")
            await asyncio.sleep(5)

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
