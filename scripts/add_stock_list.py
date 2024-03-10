"""테스트"""
import asyncio
import urllib.request
import zipfile
import os
from prisma import Prisma

def kospi_master_download(base_dir: str):
    """코스피 종목 리스트 리턴"""
    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/kospi_code.mst.zip", # pylint: disable=C0301
                               base_dir + "/kospi_code.zip")

    os.chdir(base_dir)
    kospi_zip = zipfile.ZipFile('kospi_code.zip')
    kospi_zip.extractall()

    kospi_zip.close()

    if os.path.exists("kospi_code.zip"):
        os.remove("kospi_code.zip")


async def get_kospi_master_dataframe(base_dir: str, db: Prisma):
    """DB에 종목코드 써 넣기"""
    file_name = base_dir + "/kospi_code.mst"

    with open(file_name, mode="r", encoding="cp949") as f:
        for row in f:
            rf1 = row[0:len(row) - 228]
            rf1_1 = rf1[0:9].rstrip()
            rf1_3 = rf1[21:].strip()
            if rf1_1.isdigit() is True:
                print(rf1_1, rf1_3)
                # rf2 = row[-228:] 
                try:
                    await db.stock.create(
                         {
                            'stock_name': rf1_3,
                            'stock_code': rf1_1,
                        }
                    )
                except Exception as e: # pylint: disable=W0702 W0718
                    print(e)

    # part1_columns = ['단축코드', '표준코드', '한글명']

    # field_specs = [2, 1, 4, 4, 4,
    #                1, 1, 1, 1, 1,
    #                1, 1, 1, 1, 1,
    #                1, 1, 1, 1, 1,
    #                1, 1, 1, 1, 1,
    #                1, 1, 1, 1, 1,
    #                1, 9, 5, 5, 1,
    #                1, 1, 2, 1, 1,
    #                1, 2, 2, 2, 3,
    #                1, 3, 12, 12, 8,
    #                15, 21, 2, 7, 1,
    #                1, 1, 1, 1, 9,
    #                9, 9, 5, 9, 8,
    #                9, 3, 1, 1, 1
    #                ]

    # part2_columns = ['그룹코드', '시가총액규모', '지수업종대분류', '지수업종중분류', '지수업종소분류',
    #                  '제조업', '저유동성', '지배구조지수종목', 'KOSPI200섹터업종', 'KOSPI100',
    #                  'KOSPI50', 'KRX', 'ETP', 'ELW발행', 'KRX100',
    #                  'KRX자동차', 'KRX반도체', 'KRX바이오', 'KRX은행', 'SPAC',
    #                  'KRX에너지화학', 'KRX철강', '단기과열', 'KRX미디어통신', 'KRX건설',
    #                  'Non1', 'KRX증권', 'KRX선박', 'KRX섹터_보험', 'KRX섹터_운송',
    #                  'SRI', '기준가', '매매수량단위', '시간외수량단위', '거래정지',
    #                  '정리매매', '관리종목', '시장경고', '경고예고', '불성실공시',
    #                  '우회상장', '락구분', '액면변경', '증자구분', '증거금비율',
    #                  '신용가능', '신용기간', '전일거래량', '액면가', '상장일자',
    #                  '상장주수', '자본금', '결산월', '공모가', '우선주',
    #                  '공매도과열', '이상급등', 'KRX300', 'KOSPI', '매출액',
    #                  '영업이익', '경상이익', '당기순이익', 'ROE', '기준년월',
    #                  '시가총액', '그룹사코드', '회사신용한도초과', '담보대출가능', '대주가능'
    #                  ]
    print("Done")
    os.remove(file_name)


async def main() -> None:
    """
    a
    """
    db = Prisma()
    await db.connect()
    base_dir = os.getcwd()
    kospi_master_download(base_dir)
    await db.stock.delete_many()
    await get_kospi_master_dataframe(base_dir, db)
    await db.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
    