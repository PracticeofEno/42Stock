"""테스트"""
import asyncio
from classes.ksi_api import KsiApi
import xml.etree.ElementTree as ET

async def main():
    """
    a
    """
    # access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjQxY2QxN2VlLTBiNjItNDdiMy1iMmVmLTE0ODJhMTFiOWVjMSIsImlzcyI6InVub2d3IiwiZXhwIjoxNzExMzgwNTMwLCJpYXQiOjE3MTEyOTQxMzAsImp0aSI6IlBTeklrNTR4ZGNoakJyU21rczhVMWYwam5mVzRBdzZYU0pxNCJ9.az3guQ38vv-6L3iQgJHBhD0cwqKyrgJH-eyirAF0eHamvuzWBycfk1dOSnulYjntyfinlBUhCUjG-orcMf6VfA" # pylint: disable=C0301
    # ksi_api_client = KsiApi(access_token)
    # await ksi_api_client.set_credentails()
    # result = await ksi_api_client.get_current_price("005930")
    # print(result)
    tree = ET.parse('dart/CORPCODE.xml')
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
        print("corp_code:", corp_code)
        print("corp_name:", corp_name)
        print("stock_code:", stock_code)
        print("modify_date:", modify_date)
        count += 1
    print(count)



if __name__ == '__main__':
    asyncio.run(main())
