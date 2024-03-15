# 한국투자증권 API를 이용한 토이스탁

## 환경 및 실행방법
- linux
- postgresql
- prisma
리눅스에서 postgresql, python, prisma 설치 후 pipenv install 로 의존성 설치
이후 crontab에 add_stock_list.sh, add_today_price.sh 등록

## 프로젝트 구조
- classes: 코드에 사용될 클래스 정의 모음
- scripts: crontab 에 등록되거나 사용할 script 모음

## 각 클래스별 역할
- ksi_api : 한국투자증권 api를 사용하여 필요한 정보만을 함수로 만들어 json이나 list[json] 형태로 반환
- moving_average: 이평선에 대한 클래스. 차후 상위 클래스에 포함될 예정
- stock_db: DB접근 클래스. 작업의 일관성을 위하여 DB관련된 조작은 StockDB클래스를 통하여 함

## 각 스크립트 역할
- add_stock_list.sh : 종목리스트에서 상폐된 종목 DB에서 제거 및 상장된 종목 추가
- add_today_price.sh : 매일 종가 데이터 가져와서 이평선 계산해서 추가

