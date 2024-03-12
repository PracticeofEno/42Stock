"""KSI APi Class"""
import os
import requests

class KsiApi:
    """KSI Api Class"""
    def __init__(self, at: str = ""):
        self.vts = os.getenv('VIR_VTS', '')
        self.app_key = os.getenv('VIR_APP_KEY', '')
        self.app_secret = os.getenv('VIR_APP_SECRET', '')
        self.access_token = at
        print(self.vts, self.app_key, self.app_secret)

    async def get_v_token(self):
        """일봉데이터 가져오기"""
        if self.vts == '' or self.app_key == '' or self.app_secret == '':
            print("vts, app_key, app_secret not found. check .env file.")
            return
        url = self.vts + "/oauth2/tokenP"
        response = requests.post(url=url, json={
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }, headers={
            "content-type": "application/json",
        },timeout=5)
        if response.status_code != 200:
            print(response.status_code)
            return
        res = response.json()
        self.access_token = res['access_token']
        print(self.access_token)

    async def get_daily_data(self, stock_code: str):
        """일봉데이터 가져오기"""
        if self.access_token == "":
            print("access_token not found. must call get_v_token() before function")
            return
        fid_cond_mrkt_div_code = "J" # 시장 분류 코드
        fid_input_iscd = stock_code # 종목 코드
        fid_input_date_1 = "20200101" # 시작일자 (20220501)
        #(한 번의 호출에 최대 100건의 데이터 수신, 다음 데이터를 받아오려면
        # OUTPUT 값의 가장 과거 일자의 1일 전 날짜를 FID_INPUT_DATE_2에 넣어 재호출)
        fid_input_date_2 = "20240308" # 종료 일자
        fid_period_div_code = "D" # 기간 분류 코드(D:일봉, W:주봉, M:월봉, Y:년봉)
        fid_org_adj_prc = "1"
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + self.access_token,
            'appkey': self.app_key,
            'appsecret': self.app_secret,
            'tr_id': 'FHKST03010100'
        }
        
        last_day = "20240308"
        # 받아온 데이터
        while last_day >= fid_input_date_1:
            url = f"{self.vts}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice?fid_cond_mrkt_div_code={fid_cond_mrkt_div_code}&fid_input_iscd={fid_input_iscd}&fid_input_date_1={fid_input_date_1}&fid_input_date_2={fid_input_date_2}&fid_period_div_code={fid_period_div_code}&fid_org_adj_prc={fid_org_adj_prc}"
            response = requests.get(url=url, headers=headers, timeout=5)
            if response.status_code == 200:
                res_json= response.json()
                stock_name = res_json['output1']['hts_kor_isnm']
                dailys = res_json['output2']
                for daily in dailys:
                    if 'stck_bsop_date' not in daily:
                        print(f'{stock_code} is done')
                        last_day = str(int(fid_input_date_1) - 1)
                        break
                    try:
                        await self.repo.create_daily_data(
                            stock_name=stock_name,
                            stck_bsop_date=daily['stck_bsop_date'],
                            stck_clpr=daily['stck_clpr'],
                            stck_oprc=daily['stck_oprc'],
                            stck_hgpr=daily['stck_hgpr'],
                            stck_lwpr=daily['stck_lwpr'],
                            volume=daily['acml_vol'],
                            mount=daily['acml_tr_pbmn']
                        )
                    except: # pylint: disable=W0702
                        pass
                    last_day = daily['stck_bsop_date']
            fid_input_date_2 = str(int(last_day) - 1)

    async def get_today_data(self, stock_code: str, day: str):
        """일봉데이터 가져오기"""
        if self.access_token == "":
            print("access_token not found. must call get_v_token() before function")
            return
        fid_cond_mrkt_div_code = "J" # 시장 분류 코드
        fid_input_iscd = stock_code # 종목 코드
        fid_input_date_1 = day # 시작일자 (20220501)
        #(한 번의 호출에 최대 100건의 데이터 수신, 다음 데이터를 받아오려면
        # OUTPUT 값의 가장 과거 일자의 1일 전 날짜를 FID_INPUT_DATE_2에 넣어 재호출)
        fid_input_date_2 = day # 종료 일자
        fid_period_div_code = "D" # 기간 분류 코드(D:일봉, W:주봉, M:월봉, Y:년봉)
        fid_org_adj_prc = "1"
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + self.access_token,
            'appkey': self.app_key,
            'appsecret': self.app_secret,
            'tr_id': 'FHKST03010100'
        }

        # 받아온 데이터
        url = f"{self.vts}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice?fid_cond_mrkt_div_code={fid_cond_mrkt_div_code}&fid_input_iscd={fid_input_iscd}&fid_input_date_1={fid_input_date_1}&fid_input_date_2={fid_input_date_2}&fid_period_div_code={fid_period_div_code}&fid_org_adj_prc={fid_org_adj_prc}"
        response = requests.get(url=url, headers=headers, timeout=5)
        if response.status_code == 200:
            res_json= response.json()
            stock_name = res_json['output1']['hts_kor_isnm']
            dailys = res_json['output2']
            for daily in dailys:
                if 'stck_bsop_date' in daily:
                    if daily['stck_bsop_date'] != day:
                        print(f'{stock_code} is not today')
                        break
                    try:
                        await self.repo.create_daily_data(
                            stock_name=stock_name,
                            stck_bsop_date=daily['stck_bsop_date'],
                            stck_clpr=daily['stck_clpr'],
                            stck_oprc=daily['stck_oprc'],
                            stck_hgpr=daily['stck_hgpr'],
                            stck_lwpr=daily['stck_lwpr'],
                            volume=daily['acml_vol'],
                            mount=daily['acml_tr_pbmn']
                        )
                    except Exception as e: # pylint: disable=W0702
                        print(str(e))
                        break
