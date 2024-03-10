"""테스트"""
import asyncio
from prisma import Prisma

async def main() -> None:
    """
    a
    """
    db = Prisma()
    await db.connect()
    stocks = await db.stock.find_many()
    print(stocks)



if __name__ == '__main__':
    asyncio.run(main())
    