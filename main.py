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

    selected_list = []
    # 전 종목 반복
    for stock in stocks:
        # 240일치 데이터를 가져오기
        dailys = await db_stock.get_daily_by_stock_name(stock.stock_name, "20240313", 60)
        check_ma_df = True
        miss_count = 0
        # 240일치 이평선 만들기
        if len(dailys) == 0 :
            continue
        for daily in dailys:
            if check_ma_difference(daily.mov_5, daily.mov_20, daily.mov_60, 1.05) is False:
                miss_count += 1
        if ((60 - miss_count) / 60) > 0.9:
            selected_list.append({
                'stock_name' : stock.stock_name,
                'stock_code' : stock.stock_code
            })
            print(stock.stock_name, stock.stock_code)
    print("done")

def check_ma_difference(ma_1: float, ma_2: float, ma_3: float, c: float):
    """두 이평선 최대값과 최소값의 차이가 최소값에서 min * c > max인지 확인"""
    min_val = min(ma_1, ma_2, ma_3)
    max_val = max(ma_1, ma_2, ma_3)
    if min_val * c > max_val:
        return True
    else:
        return False


if __name__ == '__main__':
    asyncio.run(main())
    