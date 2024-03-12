"""테스트"""
import asyncio
import sys
import os
# 다른폴더에 있는 py를 import하기 위한 설정
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from classes import ksi_api, stcok_db, moving_average # pylint: disable=C0413
async def main():
    """
    a
    """
    # v_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImVjMzdjNjI5LWJkMDEtNDE4Zi04ODUxLWY2MDhmZjMxNDUzOCIsImlzcyI6InVub2d3IiwiZXhwIjoxNzEwMzIxNjgzLCJpYXQiOjE3MTAyMzUyODMsImp0aSI6IlBTeklrNTR4ZGNoakJyU21rczhVMWYwam5mVzRBdzZYU0pxNCJ9.0jLCei-TF3pojxzw6_iidI-Kj5iO4JH0fmc4S95eWwTSCXwFaFjUqYlbFCLFODSQi28E5Sb7g99bPEYbu7QKSg"
    # ksi_api_client = ksi_api.KsiApi(v_token)
    # await ksi_api_client.get_v_token()
    # response = await ksi_api_client.get_all_daily_data("005930")

    db_stock = stcok_db.StockDB()
    await db_stock.connect()
    # stocks = await repo.get_stock_list()
    # mov_5 = MovingAverage(5)
    # mov_10 = MovingAverage(10)
    # mov_20 = MovingAverage(20)
    # mov_60 = MovingAverage(60)
    # mov_120 = MovingAverage(120)
    # mov_240 = MovingAverage(240)
    # for stock in stocks:
    #     dailys = await repo.get_daily_by_stock_name(stock.stock_name)
    #     for daily in dailys:
    #         mov_5.push_data(daily.stck_clpr)
    #         mov_10.push_data(daily.stck_clpr)
    #         mov_20.push_data(daily.stck_clpr)
    #         mov_60.push_data(daily.stck_clpr)
    #         mov_120.push_data(daily.stck_clpr)
    #         mov_240.push_data(daily.stck_clpr)

    #         await repo.update_mov_value(
    #             stock.stock_name,
    #             daily.stck_bsop_date,
    #             mov_5.get_moving_average(),
    #             mov_10.get_moving_average(),
    #             mov_20.get_moving_average(),
    #             mov_60.get_moving_average(),
    #             mov_120.get_moving_average(),
    #             mov_240.get_moving_average()
    #         )
    #     print(f'{stock.stock_name} daily moving average done')
    print("done")



if __name__ == '__main__':
    asyncio.run(main())
    