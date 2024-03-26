"""KSI APi Class"""
import os
from datetime import datetime
import requests
from dart.dart_mixin import DartApiMixin
from classes.stcok_db import StockDB

class DartApi(DartApiMixin):
    """KSI Api Class"""
    def __init__(self):
        self.app_key = ""
        self.stock_db = StockDB()

    async def db_connect(self):
        """DB 연결"""
        await self.stock_db.connect()

    async def search_disclosure(self, date: str):
        """공시 검색"""
        response = await super().search_disclosure(date)
        print(response)
