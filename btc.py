import requests
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

API_KEY = os.getenv("CCDATA_API_KEY")
SYMBOL = "BTC-USD"
MARKET = "ccix"
URL = f"https://data-api.cryptocompare.com/index/cc/v1/latest/tick?market={MARKET}&instruments={SYMBOL}&api_key={API_KEY}"

README_PATH = "README.md"

def get_crypto_price():
    """ccdata.io API를 호출하여 비트코인(BTC)의 현재 가격 데이터를 가져옴"""
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        try:
            # JSON 응답의 정확한 구조로 접근
            price_data = data["Data"][SYMBOL]
            price = price_data["VALUE"]  # 현재 가격
            high = price_data["CURRENT_DAY_HIGH"]  # 24시간 최고가
            low = price_data["CURRENT_DAY_LOW"]  # 24시간 최저가

            return f"BTC/USD\n 현재 가격: ${price}\n 최고가: ${high}\n 최저가: ${low}\n"
        except KeyError:
            return "API 응답에서 예상하지 못한 데이터 구조입니다."
    else:
        return f"API 요청 실패 (상태 코드: {response.status_code})"

def update_readme():
    """README.md 파일을 업데이트"""
    crypto_info = get_crypto_price()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
# Crypto Price Status

이 리포지토리는 ccdata.io API를 사용하여 비트코인(BTC)의 가격 정보를 자동으로 업데이트합니다.

## 현재 비트코인 가격
> {crypto_info}

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    while True:
        update_readme()
        print("README.md 파일이 업데이트되었습니다.")
        time.sleep(300)  # 5분 대기
