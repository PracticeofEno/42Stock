"""테스트"""
import asyncio
# from classes.ksi_api import KsiApi
from classes.stcok_db import StockDB

async def main():
    """
    a
    """
    # v_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImVjMzdjNjI5LWJkMDEtNDE4Zi04ODUxLWY2MDhmZjMxNDUzOCIsImlzcyI6InVub2d3IiwiZXhwIjoxNzEwMzIxNjgzLCJpYXQiOjE3MTAyMzUyODMsImp0aSI6IlBTeklrNTR4ZGNoakJyU21rczhVMWYwam5mVzRBdzZYU0pxNCJ9.0jLCei-TF3pojxzw6_iidI-Kj5iO4JH0fmc4S95eWwTSCXwFaFjUqYlbFCLFODSQi28E5Sb7g99bPEYbu7QKSg"
    # ksi_api_client = KsiApi(v_token)
    # await ksi_api_client.get_v_token()
    db_stock = StockDB()
    await db_stock.connect()

    stocks = await db_stock.get_stock_list()

    selected_list = []
    # 전 종목 반복
    for stock in stocks:
        # 240일치 데이터를 가져오기
        dailys = await db_stock.get_daily_by_stock_name(stock.stock_name, "20240316", 60)
        dailys.reverse()
        count = 0
        for daily in dailys:
            if check_difference(daily.mov_5, daily.stck_clpr, 5):
                count +=1
        if count > 60 * 0.9:
            selected_list.append(stock.stock_name)
            print(stock.stock_name)
    print("done")

def check_difference(ma_5, ma_10, percent):
    """시가와 종가의 차이가 percent 이하인지 확인"""
    difference = abs(ma_5 - ma_10)
    percentage_difference = (difference / max(ma_5, ma_10)) * 100
    return percentage_difference <= percent

if __name__ == '__main__':
    asyncio.run(main())
