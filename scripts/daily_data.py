"""테스트"""
import asyncio
import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from classes import stcok_db, ksi_api, moving_average # pylint: disable=C0413
async def main():
    """
    a
    """
    v_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjBlOWZkOGEwLTg5OWYtNDMzZC04MmVlLWMzZjlkNWY3MWI1OCIsImlzcyI6InVub2d3IiwiZXhwIjoxNzEwNjAwNjQ1LCJpYXQiOjE3MTA1MTQyNDUsImp0aSI6IlBTeklrNTR4ZGNoakJyU21rczhVMWYwam5mVzRBdzZYU0pxNCJ9.CrQC36oPoQMJSbf5e0TdMBCyrINnzUqXbhBCTV8DSYwOjuOdAPauwUVZXHO1Ulty7YzxJBzgMhePWy-FqOf-XQ"
    ksi_api_client = ksi_api.KsiApi()
    ksi_api_client.access_token = v_token
    await ksi_api_client.get_v_token()
    db_stock = stcok_db.StockDB()
    await db_stock.connect()

    stocks = await db_stock.get_stock_list()
    today = datetime.today().strftime('%Y%m%d')
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
        dailys_240 = await db_stock.get_daily_by_stock_name(stock.stock_name, today)
        # 240일치 이평선 만들기
        for daily in dailys_240:
            mov_5.push_data(daily.stck_clpr)
            mov_10.push_data(daily.stck_clpr)
            mov_20.push_data(daily.stck_clpr)
            mov_60.push_data(daily.stck_clpr)
            mov_120.push_data(daily.stck_clpr)
            mov_240.push_data(daily.stck_clpr)
            volume_5.push_data(daily.volume)
            volume_10.push_data(daily.volume)
            volume_20.push_data(daily.volume)
        # 오늘 데이터를 가져오기
        today_data = await ksi_api_client.get_today_data(stock.stock_code)
        # 이평선 갱신
        mov_5.push_data(float(today_data['stck_clpr']))
        mov_10.push_data(float(today_data['stck_clpr']))
        mov_20.push_data(float(today_data['stck_clpr']))
        mov_120.push_data(float(today_data['stck_clpr']))
        mov_240.push_data(float(today_data['stck_clpr']))
        volume_5.push_data(float(today_data['volume']))
        volume_10.push_data(float(today_data['volume']))
        volume_20.push_data(float(today_data['volume']))
        await db_stock.create_today_data(
            stock.stock_name,
            today_data['stck_bsop_date'],
            float(today_data['stck_clpr']),
            float(today_data['stck_oprc']),
            float(today_data['stck_hgpr']),
            float(today_data['stck_lwpr']),
            float(today_data['volume']),
            float(today_data['mount']),
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
        print(f'{stock.stock_name} daily data inserted')
    print("done")


if __name__ == '__main__':
    asyncio.run(main())
    