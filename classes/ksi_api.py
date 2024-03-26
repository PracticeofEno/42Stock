"""KSI APi Class"""
import os
from datetime import datetime
import requests
from classes.api_mixin import KSIApiMixin

class KsiApi(KSIApiMixin):
    """KSI Api Class"""
    def __init__(self, access_token: str = ""):
        self.app_key = ""
        self.app_secret = ""
        self.vts = ""
        if access_token != "":
            self.access_token = access_token

    async def set_credentails(self):
        """Mixin을 사용하여 환경변수와 액세스토큰 설정"""
        self.get_credentials()

    async def get_current_price(self, stock_code: str):
        """현재 주식 가격 가져오기"""
        return await super().get_current_price(stock_code)

    async def get_stock_info(self, stock_code: str):
        """주식 기본 정보 조회"""
        return await super().stock_info(stock_code)

    async def check_delisting(self, stock_code:str) -> bool:
        """종목의 상폐여부 조회"""
        data = await self.get_stock_info(stock_code)
        stock_info = data['output']
        if stock_info['scts_mket_lstg_abol_dt'] == "":
            return True
        return False

    async def get_all_daily_data(
        self,
        stock_code: str,
        start_date: str = "20200101",
        end_date: str = datetime.today().strftime('%Y%m%d')):
        """
        일봉데이터 가져오기
        start_date: 시작일자 (ex.20200101)
        end_date: 종료 일자 (ex.20240308)
        """
        start_day = start_date
        last_day = end_date
        res_list = []
        # 받아온 데이터
        while last_day >= start_day:
            res_json = await super().get_all_daily_data(stock_code, start_day, last_day)
            stock_name = res_json['output1']['hts_kor_isnm']
            dailys = res_json['output2']
            for daily in dailys:
                if 'stck_bsop_date' not in daily:
                    print(f'{stock_code} is done')
                    last_day = str(int(start_day) - 1)
                    break
                res_list.append({
                    "stock_name": stock_name,
                    "stck_bsop_date": daily['stck_bsop_date'],
                    "stck_clpr": daily['stck_clpr'],
                    "stck_oprc": daily['stck_oprc'],
                    "stck_hgpr": daily['stck_hgpr'],
                    "stck_lwpr": daily['stck_lwpr'],
                    "volume": daily['acml_vol'],
                    "mount": daily['acml_tr_pbmn']
                })
                last_day = daily['stck_bsop_date']
            last_day = str(int(last_day) - 1)
        return res_list

    async def get_today_data(self, stock_code: str):
        """오늘 날짜의 종목 데이터 가져오기"""
        response = await super().get_current_price(stock_code)
        data = response['output']
        return data

    async def check_available_trade(self, stock_code:str):
        """주식 기본 조회"""
        if self.access_token == "":
            print("access_token not found. must call get_v_token() before function")
            return

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + self.access_token,
            'appkey': self.app_key,
            'appsecret': self.app_secret,
            'tr_id': 'CTPF1002R',
            'custtype': 'P'
        }

        # 받아온 데이터
        url = f"{self.vts}/uapi/domestic-stock/v1/quotations/search-stock-info?PDNO={stock_code}&PRDT_TYPE_CD=300" # pylint: disable=C0301
        response = requests.get(url=url, headers=headers, timeout=5)
        if response.status_code == 200:
            res_json= response.json()
            trade = res_json['output']['tr_stop_yn']
            if trade == "Y":
                return False
            else:
                return True
            