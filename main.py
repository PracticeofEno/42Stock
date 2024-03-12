"""테스트"""
import asyncio
from prisma import Prisma
from classes.ksi_api import KsiApi
from classes.stcok_db import Repository
from classes.moving_average import MovingAverage

async def main():
    """
    a
    """
    db = Prisma()
    await db.connect()
    repo = Repository(db)
    stocks = await repo.get_stock_list()
    mov_5 = MovingAverage(5)
    mov_10 = MovingAverage(10)
    mov_20 = MovingAverage(20)
    mov_60 = MovingAverage(60)
    mov_120 = MovingAverage(120)
    mov_240 = MovingAverage(240)
    for stock in stocks:
        dailys = await repo.get_daily_by_stock_name(stock.stock_name)
        for daily in dailys:
            mov_5.push_data(daily.stck_clpr)
            mov_10.push_data(daily.stck_clpr)
            mov_20.push_data(daily.stck_clpr)
            mov_60.push_data(daily.stck_clpr)
            mov_120.push_data(daily.stck_clpr)
            mov_240.push_data(daily.stck_clpr)

            await repo.update_mov_value(
                stock.stock_name,
                daily.stck_bsop_date,
                mov_5.get_moving_average(),
                mov_10.get_moving_average(),
                mov_20.get_moving_average(),
                mov_60.get_moving_average(),
                mov_120.get_moving_average(),
                mov_240.get_moving_average()
            )
        print(f'{stock.stock_name} daily moving average done')
    print("done")



if __name__ == '__main__':
    asyncio.run(main())
    