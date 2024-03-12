"""테스트"""
import asyncio
from datetime import datetime
from prisma import Prisma
from classes.ksi_api import KsiApi
from classes.stcok_db import StockDB
from classes.moving_average import MovingAverage

async def main():
    """
    a
    """
    v_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImVjMzdjNjI5LWJkMDEtNDE4Zi04ODUxLWY2MDhmZjMxNDUzOCIsImlzcyI6InVub2d3IiwiZXhwIjoxNzEwMzIxNjgzLCJpYXQiOjE3MTAyMzUyODMsImp0aSI6IlBTeklrNTR4ZGNoakJyU21rczhVMWYwam5mVzRBdzZYU0pxNCJ9.0jLCei-TF3pojxzw6_iidI-Kj5iO4JH0fmc4S95eWwTSCXwFaFjUqYlbFCLFODSQi28E5Sb7g99bPEYbu7QKSg"
    ksi_api_client = KsiApi(v_token)
    await ksi_api_client.get_v_token()
    db_stock = StockDB()
    await db_stock.connect()

    stocks = await db_stock.get_stock_list()
    mov_5 = MovingAverage(5)
    mov_10 = MovingAverage(10)
    mov_20 = MovingAverage(20)
    mov_60 = MovingAverage(60)
    mov_120 = MovingAverage(120)
    mov_240 = MovingAverage(240)
    volume_5 = MovingAverage(5)
    volume_10 = MovingAverage(10)
    volume_20 = MovingAverage(20)

    # 전 종목 반복
    for stock in stocks:
        # 240일치 데이터를 가져오기
        dailys = await db_stock.get_daily_by_stock_name(stock.stock_name)
        # 240일치 이평선 만들기
        for daily in dailys:
            mov_5.push_data(daily.stck_clpr)
            mov_10.push_data(daily.stck_clpr)
            mov_20.push_data(daily.stck_clpr)
            mov_60.push_data(daily.stck_clpr)
            mov_120.push_data(daily.stck_clpr)
            mov_240.push_data(daily.stck_clpr)
            volume_5.push_data(daily.volume)
            volume_10.push_data(daily.volume)
            volume_20.push_data(daily.volume)
            await db_stock.update_mov_value(
                stock.stock_name,
                daily.stck_bsop_date,
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
    