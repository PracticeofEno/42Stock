"""API를 MIXIN 형태로 사용하게 변경하기 위한 클래스"""
import os
from datetime import datetime
import requests

def checking_env(func):
    """
    환경변수 체크 데코레이터
    없다면 .env 파일에서 가져옴
    """
    def wrapper(self, *args, **kwargs):
        if not (hasattr(self, 'vts') and hasattr(self, 'app_key') and hasattr(self, 'app_secret')):
            self.vts = os.getenv('VIR_VTS')
            self.app_key = os.getenv('VIR_APP_KEY')
            self.app_secret = os.getenv('VIR_APP_SECRET')
        elif self.vts == '' or self.app_key == '' or self.app_secret == '':
            self.vts = os.getenv('VIR_VTS')
            self.app_key = os.getenv('VIR_APP_KEY')
            self.app_secret = os.getenv('VIR_APP_SECRET')
            return func(self, *args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper

def checking_access_token(func):
    """
    access_token 체크 데코레이터
    없다면 get_v_token() 호출
    """
    def wrapper(self, *args, **kwargs):
        if hasattr(self, 'access_token') is False:
            self.access_token = get_access_token(self.vts, self.app_key, self.app_secret)
        else:
            if check_request(self.access_token, self.app_key, self.app_secret) is False:
                self.access_token = get_access_token(self.vts, self.app_key, self.app_secret)
        return func(self, *args, **kwargs)
    return wrapper

def check_request(access_token: str, app_key: str, app_secret: str):
    """현재가격 가져오기"""
    url = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-price?fid_cond_mrkt_div_code=J&fid_input_iscd=005930" # pylint: disable=C0301
    payload = ""
    headers = {
        'content-type': 'application/json',
        'authorization': 'Bearer ' + access_token,
        'appkey': app_key,
        'appsecret': app_secret,
        'tr_id': 'FHKST03010100'
    }
    response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
    if response.status_code == 200:
        return True
    return False

def get_access_token(vts: str, app_key: str, app_secret: str):
    """한투증권 서버로부터 access_token을 받아오는 함수"""
    url = vts + "/oauth2/tokenP"
    response = requests.post(url=url, json={
        "grant_type": "client_credentials",
        "appkey": app_key,
        "appsecret": app_secret
    }, headers={
        "content-type": "application/json",
    },timeout=5)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception("get access_token failed") # pylint: disable=C0415 W0719
    res = response.json()
    return res['access_token']

class KSIApiMixin:
    """Mixin 클래스"""

    @checking_env
    @checking_access_token
    def get_credentials(self):
        """액세스 토큰을 얻기 위한 함수"""
        print(self.vts, self.app_key, self.app_secret)
        print(self.access_token)
        # if access_token != "":
        #     self.access_token = access_token
        # else:
        #     self.access_token = ""

    async def get_current_price(self, stock_code: str):
        """현재 주식 가격을 가져옴"""
        url = f"{self.vts}/uapi/domestic-stock/v1/quotations/inquire-price?fid_cond_mrkt_div_code=J&fid_input_iscd={stock_code}" # pylint: disable=C0301
        payload = ""
        headers = {
            'content-type': 'application/json',
            'authorization': f"Bearer {self.access_token}",
            'appkey': self.app_key,
            'appsecret': self.app_secret,
            'tr_id': 'FHKST01010100'
        }
        response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
        if response.status_code == 200:
            res_json = response.json()
            return res_json
        raise Exception(f'{stock_code} get_current_price failed') # pylint: disable=C0415 W0719

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
        fid_cond_mrkt_div_code = "J" # 시장 분류 코드
        fid_input_iscd = stock_code # 종목 코드
        fid_input_date_1 = start_date # 시작일자 (20220501)
        #(한 번의 호출에 최대 100건의 데이터 수신, 다음 데이터를 받아오려면
        # OUTPUT 값의 가장 과거 일자의 1일 전 날짜를 FID_INPUT_DATE_2에 넣어 재호출)
        fid_input_date_2 = end_date # 종료 일자
        fid_period_div_code = "D" # 기간 분류 코드(D:일봉, W:주봉, M:월봉, Y:년봉)
        fid_org_adj_prc = "1"
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + self.access_token,
            'appkey': self.app_key,
            'appsecret': self.app_secret,
            'tr_id': 'FHKST03010100'
        }

        url = f"{self.vts}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice?fid_cond_mrkt_div_code={fid_cond_mrkt_div_code}&fid_input_iscd={fid_input_iscd}&fid_input_date_1={fid_input_date_1}&fid_input_date_2={fid_input_date_2}&fid_period_div_code={fid_period_div_code}&fid_org_adj_prc={fid_org_adj_prc}" # pylint: disable=C0301
        response = requests.get(url=url, headers=headers, timeout=5)
        if response.status_code == 200:
            res_json= response.json()
            return res_json
        else:
            raise Exception(f'{stock_code} get_all_daily_data failed') # pylint: disable=C0415 W0719
