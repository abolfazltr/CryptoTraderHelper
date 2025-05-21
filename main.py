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
        sys.stdout.flush()

        # دریافت قیمت
        try:
            price = get_current_price(token)
            print(f"✅ قیمت فعلی {token.upper()}: {price}")
        except Exception as e:
            if "ConnectionError" in str(e) or "NameResolutionError" in str(e):
                print(f"❌ خطا در اتصال به صرافی برای {token.upper()}: {e}")
            else:
                print(f"❌ خطا در دریافت قیمت {token.upper()}: {e}")
            sys.stdout.flush()
            continue

        # تحلیل تکنیکال
        try:
            print("🔎 تحلیل تکنیکال در حال انجام است...")
            signal = analyze_token(token)
            print(f"🔍 سیگنال تحلیل شده: {signal}")
        except Exception as e:
            print(f"❌ خطا در تحلیل تکنیکال {token.upper()}: {e}")
            sys.stdout.flush()
            continue

        # اجرای پوزیشن در صورت وجود سیگنال
        if signal:
            print(f"🚀 سیگنال معتبر برای {token.upper()} به صورت {signal.upper()}")
            try:
                tx_hash = open_position(token, signal)
                print(f"✅ پوزیشن واقعی باز شد | TX Hash: {tx_hash}")
            except Exception as e:
                print(f"❌ خطا در باز کردن پوزیشن: {e}")
        else:
            print(f"❌ هیچ سیگنالی برای {token.upper()} صادر نشده.")

        sys.stdout.flush()

    print("⏳ منتظر اجرای بعدی در ۵ دقیقه...\n")
    sys.stdout.flush()
    time.sleep(300)