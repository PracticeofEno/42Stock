"""매일 장 마감 후 실행되는 스크립트. 당일 데이터를 수집하는걸 목표로 함"""
import asyncio
import sys
import os
from datetime import datetime
from prisma import Prisma
# 다른폴더에 있는 py를 import하기 위한 설정
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from classes import ksi_api, repository # pylint: disable=C0413

async def main() -> None:
    """
    a
    """
    db = Prisma()
    await db.connect()
    repo = repository.Repository(db)

    tmp = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjdjN2U3MzkyLTFiZDktNDQyOS05ODc0LTRkMDhkZDg3OGE5ZCIsImlzcyI6InVub2d3IiwiZXhwIjoxNzEwMTY0MjY1LCJpYXQiOjE3MTAwNzc4NjUsImp0aSI6IlBTeklrNTR4ZGNoakJyU21rczhVMWYwam5mVzRBdzZYU0pxNCJ9.AhAZybgII5NNDs7Tpa8R6ZapFbMEePyjYQLUuDmwwQjK09zpPcLxlv-vYeBJqaRnyRgVTHefuG6-6hyF8ud4OQ"
    ksi_api_client =  ksi_api.KsiApi(tmp, repo)
    # await ksi_api2.get_v_token()
    # print(res)
    stocks = await ksi_api_client.get_stock_list()
    today = datetime.today().strftime('%Y%m%d')
    print(today)
    for stock in stocks:
        await ksi_api_client.get_today_data(stock.stock_code, today)
        print(f'{stock.stock_name} done')
    print("done")



if __name__ == '__main__':
    asyncio.run(main())
    