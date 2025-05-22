import time
import sys
from utils.strategy import analyze_token
from utils.gmx_v2 import open_position

TOKENS = ["eth", "link"]
NAMES = {"eth": "E", "link": "S"}

while True:
    print("\n==============================")
    print("🕓 شروع بررسی بازار...\n")
    sys.stdout.flush()

    summary = []  # برای چاپ خلاصه آخر کار

    for token in TOKENS:
        symbol = NAMES[token]
        print(f"📊 بررسی توکن: {token.upper()} ({symbol})")

        try:
            signal = analyze_token(token)
        except Exception as e:
            print(f"❌ خطا در تحلیل {symbol}: {e}")
            summary.append(f"{symbol} = ERROR")
            continue

        if signal:
            print(f"🚨 سیگنال برای {symbol}: {signal.upper()}")
            try:
                df = analyze_token(token)
                if df is not None:
                    price = df["close"].iloc[-1]
                    print(f"💰 قیمت ورود: {price:.4f}")
                    open_position(token, signal == "long", price)
                    summary.append(f"{symbol} = {signal.upper()}")
                else:
                    print(f"❌ دریافت قیمت برای {symbol} ناموفق بود.")
                    summary.append(f"{symbol} = NO PRICE")
            except Exception as e:
                print(f"❌ خطا در باز کردن پوزیشن {symbol}: {e}")
                summary.append(f"{symbol} = FAIL")
        else:
            print(f"⛔ سیگنالی برای {symbol} یافت نشد.")
            summary.append(f"{symbol} = NO SIGNAL")

    print("\n🧾 خلاصه سیگنال‌ها:", " / ".join(summary))
    print("\n⏳ منتظر ۵ دقیقه بعدی...\n")
    print("==============================\n")
    time.sleep(300)