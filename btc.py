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

def get_ascii_art(change_percentage):
    """24시간 변화 퍼센트에 따라 아스키 아트를 반환"""
    if change_percentage > 0:
        return """. ᕱ__ᕱ
(⸝⸝> ̫ <⸝⸝)
♡/ ∩ ∩ \\
"""
    else:
        return """･ﾟﾟ･｡   /\\__/\\ ｡･ﾟﾟ･
｡･ﾟﾟ･( > ᴥ <) ･ﾟﾟ･｡
   (\\(__u_u)
"""

def update_readme(price_info):
    """README.md 파일을 업데이트"""
    if price_info is None:
        crypto_info = "API response does not contain the required data."
        ascii_art = ""
    else:
        current_price = price_info["current_price"]
        high_price = price_info["high_price"]
        low_price = price_info["low_price"]
        open_price = price_info["open_price"]
        change_24h = price_info["change_24h"]
        change_percentage = price_info["change_percentage"]
        volume_24h = price_info["volume_24h"]

        # 아스키 아트 선택
        ascii_art = get_ascii_art(change_percentage)

        crypto_info = (
            f"BTC/USD Current Price: ${current_price}\n"
            f"- Open Price: ${open_price}\n"
            f"- 24h High: ${high_price}\n"
            f"- 24h Low: ${low_price}\n"
            f"- 24h Change: ${change_24h} ({change_percentage}%)\n"
            f"- 24h Volume: {volume_24h} BTC"
        )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
# Crypto Price Status

This repository uses the ccdata.io API to automatically update Bitcoin (BTC) price information.

## Current Bitcoin Price
> {crypto_info}

