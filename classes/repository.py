"""repository Class"""
from prisma import Prisma

class Repository:
    """Repository Class"""
    def __init__(self, prisma: Prisma):
        self.db = prisma

    async def get_stock_list(self):
        """주식 리스트 가져오기"""
        stocks = await self.db.stock.find_many()
        return stocks

    async def create_stock(self, stock_name: str, stock_code: str):
        """주식 추가"""
        await self.db.stock.create(
            {
                'stock_name': stock_name,
                'stock_code': stock_code,
            }
        )

    async def create_daily_data(self,
                                stock_name: str,
                                stck_bsop_date: str,
                                stck_clpr: float,
                                stck_oprc: float,
                                stck_hgpr: float,
                                stck_lwpr: float,
                                volume: float,
                                mount: float):
        """일별 데이터 생성"""
        await self.db.daily.create({
            "stock_name": stock_name,
            "stck_bsop_date": stck_bsop_date,
            "stck_clpr": float(stck_clpr),
            "stck_oprc": float(stck_oprc),
            "stck_hgpr": float(stck_hgpr),
            "stck_lwpr": float(stck_lwpr),
            "volume": float(volume),
            "mount": float(mount)
        })
