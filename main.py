import time
import sys
from utils.price import get_current_price
from utils.strategy import analyze_token
from utils.gmx_v2 import open_position

TOKENS = ["eth", "link"]

while True:
    print("🕓 شروع بررسی بازار...\n")
    sys.stdout.flush()

    for token in TOKENS:
        print(f"📊 بررسی توکن: {token.upper()}")
        current_price = get_current_price(token)
        print(f"💰 قیمت لحظه‌ای: {current_price}")

        signal = analyze_token(token)
        if signal in ["long", "short"]:
            print(f"📈 سیگنال معتبر پیدا شد: {signal.upper()} برای {token.upper()}")
            open_position(token, signal)
        else:
            print("❌ هیچ سیگنال معتبری صادر نشد")

        print("-------------\n")
        time.sleep(1)

    print("⏳ در انتظار ۵ دقیقه بعدی...\n")
    time.sleep(300)