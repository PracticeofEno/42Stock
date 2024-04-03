"""API를 MIXIN 형태로 사용하게 변경하기 위한 클래스"""
from datetime import datetime
import os
import requests

def checking_env(func):
    """
    환경변수 체크 데코레이터
    없다면 .env 파일에서 가져옴
    """
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'app_key'):
            self.api_key = os.getenv('DART_API_KEY')
        elif self.app_key == '':
            self.app_key = os.getenv('DART_API_KEY')
            return func(self, *args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper

class DartApiMixin:
    """Dart Mixin 클래스"""
    @checking_env
    async def search_disclosure(self, date: str):
        """공시 검색"""
        url = (f"https://opendart.fss.or.kr/"
               f"api/list.json?crtfc_key={self.app_key}"
               f"&bgn_de={date}"
               f"&end_de={date}"
               f"&pblntf_ty=A"
               f"&page_no=1"
               f"&page_count=10")
        response = requests.get(url=url, timeout=5)
        if response.status_code == 200:
            res_json = response.json()
            return res_json
        return None
