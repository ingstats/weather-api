import requests
import time
from datetime import datetime
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

# .env 파일에서 환경 변수 로드
load_dotenv()

API_KEY = os.getenv("CCDATA_API_KEY")
SYMBOL = "BTC-USD"
MARKET = "ccix"
URL = f"https://data-api.cryptocompare.com/index/cc/v1/latest/tick?market={MARKET}&instruments={SYMBOL}&api_key={API_KEY}"

README_PATH = "README.md"
GRAPH_PATH = "crypto_price_graph.png"

def get_crypto_price():
    """ccdata.io API를 호출하여 비트코인(BTC)의 가격 데이터를 가져옴"""
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        try:
            # JSON 응답의 정확한 구조로 데이터 접근
            price_data = data["Data"][SYMBOL]
            current_price = price_data["VALUE"]
            high_price = price_data["CURRENT_DAY_HIGH"]
            low_price = price_data["CURRENT_DAY_LOW"]
            open_price = price_data["CURRENT_DAY_OPEN"]
            change_24h = price_data["CURRENT_DAY_CHANGE"]
            change_percentage = price_data["CURRENT_DAY_CHANGE_PERCENTAGE"]
            volume_24h = price_data["CURRENT_DAY_VOLUME"]

            return {
                "current_price": round(current_price, 2),
                "high_price": round(high_price, 2),
                "low_price": round(low_price, 2),
                "open_price": round(open_price, 2),
                "change_24h": round(change_24h, 2),
                "change_percentage": round(change_percentage, 2),
                "volume_24h": round(volume_24h, 2),
            }
        except KeyError:
            return None
    else:
        return None

def plot_crypto_price(current_price, high_price, low_price):
    """비트코인 가격 변화를 보여주는 간단한 막대 그래프 생성"""
    prices = [current_price, high_price, low_price]
    labels = ["현재 가격", "24시간 최고가", "24시간 최저가"]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, prices, color=['blue', 'green', 'red'])
    plt.title("비트코인(BTC) 가격 변동")
    plt.ylabel("가격 (USD)")
    plt.savefig(GRAPH_PATH)
    plt.close()

def update_readme(price_info):
    """README.md 파일을 업데이트"""
    if price_info is None:
        crypto_info = "API 응답에서 필요한 데이터를 찾을 수 없습니다."
    else:
        current_price = price_info["current_price"]
        high_price = price_info["high_price"]
        low_price = price_info["low_price"]
        open_price = price_info["open_price"]
        change_24h = price_info["change_24h"]
        change_percentage = price_info["change_percentage"]
        volume_24h = price_info["volume_24h"]

        # 그래프 생성
        plot_crypto_price(current_price, high_price, low_price)

        crypto_info = (
            f"BTC/USD 현재 가격: ${current_price}\n"
            f"- 시가: ${open_price}\n"
            f"- 24시간 최고가: ${high_price}\n"
            f"- 24시간 최저가: ${low_price}\n"
            f"- 24시간 변화량: ${change_24h} ({change_percentage}%)\n"
            f"- 24시간 거래량: {volume_24h} BTC"
        )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
# Crypto Price Status

이 리포지토리는 ccdata.io API를 사용하여 비트코인(BTC)의 가격 정보를 자동으로 업데이트합니다.

## 현재 비트코인 가격
> {crypto_info}

![비트코인 가격 변화]({GRAPH_PATH})

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    while True:
        price_info = get_crypto_price()
        update_readme(price_info)
        print("README.md 파일이 업데이트되었습니다.")
        time.sleep(120)  # 2분 대기
