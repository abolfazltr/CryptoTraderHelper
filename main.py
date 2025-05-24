import time
import sys
from datetime import datetime
from utils.price import get_current_price, get_recent_candles
from utils.strategy import analyze_token
from utils.gmx_v2 import open_position

TOKENS = ["eth", "link"]

def log(msg):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")
    sys.stdout.flush()

while True:
    log("🕓 شروع بررسی بازار...")

    for token in TOKENS:
        log(f"📊 بررسی توکن: {token.upper()}")

        try:
            candles = get_recent_candles(token)
            if candles is None or candles.empty:
                log(f"⚠️ دریافت کندل برای {token.upper()} ناموفق بود.")
                continue

            signal = analyze_token(candles)
            log(f"📈 سیگنال تحلیل شده برای {token.upper()}: {signal.upper()}")

            price = get_current_price(token)
            if price is None:
                log(f"⚠️ دریافت قیمت لحظه‌ای برای {token.upper()} ناموفق بود.")
                continue

            if isinstance(signal, str) and signal in ["long", "short"]:
                is_long = signal == "long"
                log(f"✅ اجرای پوزیشن {signal.upper()} برای {token.upper()} در قیمت {price}")
                open_position(token, is_long, price)

        except Exception as e:
            log(f"❌ خطا هنگام بررسی {token.upper()}: {e}")

    log("⏳ در حال خواب تا اجرای بعدی...\n")
    time.sleep(900)  # اجرای هر ۱۵ دقیقه