"""테스트"""
import asyncio
from prisma import Prisma
from classes.ksi_api import KsiApi
from classes.repository import Repository

async def main():
    """
    a
    """
    db = Prisma()
    await db.connect()
    repo = Repository(db)

    tmp = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjMzNjIwODQ0LTY4NDEtNGQwYy1hNDc5LTA5ODdmYzcyMGQ1YyIsImlzcyI6InVub2d3IiwiZXhwIjoxNzA5OTY1NzM5LCJpYXQiOjE3MDk4NzkzMzksImp0aSI6IlBTTWpSVjNSVmlGVUtsZmZyVGlRUVJOMTEwTHFDWGNvR3ZSMSJ9.ugFEHpiGsi7_U2tIeHEbhW6Gx960wgglQXETS0_y-hKrsaosYriezvTS3jf8PfJEqNhaSj_gUGkbCCCtaBJSLg"
    ksi_api = KsiApi(tmp, repo)
    # res = await ksi_api.get_v_token()
    # print(res)
    stocks = await ksi_api.get_stock_list()
    for stock in stocks:
        if stock.stock_code <= '253160':
            continue
        await ksi_api.get_daily_data(stock.stock_code)
    print("done")



if __name__ == '__main__':
    asyncio.run(main())
    