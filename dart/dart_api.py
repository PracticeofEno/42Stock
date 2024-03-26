"""KSI APi Class"""
import os
from datetime import datetime
import requests
from dart.dart_mixin import DartApiMixin
from classes.stcok_db import StockDB

class DartApi(DartApiMixin):
    """KSI Api Class"""
    def __init__(self):
        self.stock_db = StockDB()
        self.stock_db.connect()