"""테스트"""
import asyncio
from datetime import datetime
from prisma import Prisma
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from classes import stcok_db, ksi_api, moving_average # pylint: disable=C0413
async def main():
    """
    a
    """
    ksi_api_client = ksi_api.KsiApi()
    ksi_api_client.access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjViZjgxYzE1LWQyNDAtNDQ5NC04YjI5LThlNTExN2I1NWE0MyIsImlzcyI6InVub2d3IiwiZXhwIjoxNzEwNTUxMjM2LCJpYXQiOjE3MTA0NjQ4MzYsImp0aSI6IlBTeklrNTR4ZGNoakJyU21rczhVMWYwam5mVzRBdzZYU0pxNCJ9.P6Rl6G5thkZErh6_GUtJcONADUpLWGa4edLIii2uuwXPRzUie-olvAV3c6Z97c_uKuriOrcEd4DJJ7Dj3x7SIg"
    # await ksi_api_client.get_v_token()
    db_stock = stcok_db.StockDB()
    await db_stock.connect()
    await db_stock.delete_daily_table()

    stocks = await db_stock.get_stock_list()
    mov_5 = moving_average.MovingAverage(5)
    mov_10 = moving_average.MovingAverage(10)
    mov_20 = moving_average.MovingAverage(20)
    mov_60 = moving_average.MovingAverage(60)
    mov_120 = moving_average.MovingAverage(120)
    mov_240 = moving_average.MovingAverage(240)
    volume_5 = moving_average.MovingAverage(5)
    volume_10 = moving_average.MovingAverage(10)
    volume_20 = moving_average.MovingAverage(20)

    # 전 종목 반복
    for stock in stocks:
        # 240일치 데이터를 가져오기
        if stock.stock_code <= "004140":
            continue
        dailys = await ksi_api_client.get_all_daily_data(stock.stock_code, "20200101")
        dailys.reverse()
        # 240일치 이평선 만들기
        for daily in dailys:
            mov_5.push_data(float(daily['stck_clpr']))
            mov_10.push_data(float(daily['stck_clpr']))
            mov_20.push_data(float(daily['stck_clpr']))
            mov_60.push_data(float(daily['stck_clpr']))
            mov_120.push_data(float(daily['stck_clpr']))
            mov_240.push_data(float(daily['stck_clpr']))
            volume_5.push_data(float(daily['volume']))
            volume_10.push_data(float(daily['volume']))
            volume_20.push_data(float(daily['volume']))
            await db_stock.create_daily_data(
                stock.stock_name,
                daily['stck_bsop_date'],
                float(daily['stck_clpr']),
                float(daily['stck_oprc']),
                float(daily['stck_hgpr']),
                float(daily['stck_lwpr']),
                float(daily['volume']),
                float(daily['mount']),
                mov_5.get_moving_average(),
                mov_10.get_moving_average(),
                mov_20.get_moving_average(),
                mov_60.get_moving_average(),
                mov_120.get_moving_average(),
                mov_240.get_moving_average(),
                volume_5.get_moving_average(),
                volume_10.get_moving_average(),
                volume_20.get_moving_average()
            )
        print(f'{stock.stock_name} daily moving average done')
    print("done")


if __name__ == '__main__':
    asyncio.run(main())
    