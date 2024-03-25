"""다트의 고유번호 가져오는 파이썬 파일"""
import os
import sys
import urllib.request
import zipfile
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from classes import stcok_db, ksi_api # pylint: disable=C0413

def download_dart_code(base: str):
    """코스피 종목 리스트 리턴"""
    dart_api_key = os.getenv('DART_API_KEY')
    print(dart_api_key)
    url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={dart_api_key}"
    urllib.request.urlretrieve(url, base + "/dart/dart_code.zip")

    os.chdir(base + "/dart")
    kospi_zip = zipfile.ZipFile('dart_code.zip')
    kospi_zip.extractall()

    kospi_zip.close()

    if os.path.exists("dart_code.zip"):
        os.remove("dart_code.zip")



base_dir = os.getcwd()
download_dart_code(base_dir)
