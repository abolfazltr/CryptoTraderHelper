import time
import sys
from utils.strategy import analyze_token
from utils.price import get_current_price
from utils.gmx_v2 import open_position
from config.tokens import TOKENS

def flush_print(msg):
    print(msg)
    sys.stdout.flush()

while True:
    flush_print("\n🕓 شروع بررسی بازار...\n")
    flush_print(f"📋 لیست توکن‌ها دریافت شد: {[token['symbol'] for token in TOKENS]}")

    for token in TOKENS:
        try:
            symbol = token["symbol"]
            gmx_id = token["gmx_id"]
            coingecko_id = token["coingecko_id"]

            flush_print(f"\n📍 بررسی شروع شد برای {symbol}")
            flush_print(f"➡️ ارسال به analyze_token: {gmx_id.lower()}")

            signal = analyze_token(gmx_id.lower())

            if signal:
                flush_print(f"📡 سیگنال تحلیل دریافت شد: {signal.upper()}")
                current_price = get_current_price(gmx_id.lower())
                if current_price:
                    flush_print(f"✅ قیمت لحظه‌ای {gmx_id.upper()}: {current_price}")
                    flush_print(f"🚀 ارسال دستور پوزیشن ({signal.upper()}) برای {gmx_id.upper()}...\n")
                    open_position(gmx_id.lower(), signal == "long", current_price)
                else:
                    flush_print(f"❌ خطا در دریافت قیمت لحظه‌ای برای {gmx_id.upper()}")
            else:
                flush_print(f"⚠️ هیچ سیگنال معتبری برای {gmx_id.upper()} صادر نشد.\n")

        except Exception as e:
            flush_print(f"❌ خطای غیرمنتظره در بررسی {symbol}: {e}")

    flush_print("\n⏳ منتظر اجرای بعدی در ۵ دقیقه...\n")
    time.sleep(300)