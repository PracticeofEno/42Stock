"""repository Class"""
from prisma import Prisma

class StockDB:
    """Repository Class"""
    def __init__(self):
        db = Prisma()
        self.db = db

    async def connect(self):
        """DB에 연결"""
        await self.db.connect()

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

    async def delete_stock_table(self):
        """주식 테이블 삭제"""
        await self.db.stock.delete_many()

    async def stock_exist(self, stock_name: str):
        """종목 존재 여부 확인"""
        stock = await self.db.stock.find_first(
            where={
                'stock_name': stock_name
            }
        )
        return stock

    async def stock_remove(self, stock_name: str):
        """종목 삭제, 삭제된 종목의 일봉 데이터도 제거함"""
        await self.db.stock.delete_many(
            where={
                'stock_name': stock_name
            }
        )
        await self.db.daily.delete_many(
            where={
                'stock_name': stock_name
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

    async def get_daily_by_stock_name(self, stock_name: str):
        """특정 주식의 일별 데이터 가져오기"""
        dailys = await self.db.daily.find_many(
            where={
                'stock_name': stock_name
            },
            order={
                'stck_bsop_date': 'asc'
            }
        )
        return dailys

    async def update_mov_value(
        self,
        stock_name: str,
        stck_bsop_date: str,
        mov_5: float,
        mov_10: float,
        mov_20: float,
        mov_60: float,
        mov_120: float,
        mov_240: float
    ):
        """5일 이평선 값 업데이트"""
        await self.db.daily.update(
            where={
                'stock_name_stck_bsop_date': {
                    'stock_name': stock_name,
                    'stck_bsop_date': stck_bsop_date
                }
            },
            data={
                'mov_5': mov_5,
                'mov_10': mov_10,
                'mov_20': mov_20,
                'mov_60': mov_60,
                'mov_120': mov_120,
                'mov_240': mov_240
            }
        )
