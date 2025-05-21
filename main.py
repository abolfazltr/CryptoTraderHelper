import time
from utils.price import get_current_price
from utils.strategy import analyze_token
from utils.gmx_v2 import open_position

TOKENS = ["eth", "link"]

while True:
    print("🕓 شروع بررسی بازار...\n")

    for token in TOKENS:
        print(f"📊 بررسی {token.upper()}")

        # دریافت قیمت
        try:
            price = get_current_price(token)
            print(f"✅ قیمت فعلی {token.upper()}: {price}")
        except Exception as e:
            print(f"❌ خطا در دریافت قیمت {token.upper()}: {e}")
            continue

        # تحلیل تکنیکال
        try:
            signal = analyze_token(token)
        except Exception as e:
            print(f"❌ خطا در تحلیل {token.upper()}: {e}")
            continue

        # اجرای پوزیشن در صورت سیگنال معتبر
        if signal:
            print(f"🚀 سیگنال معتبر برای {token.upper()} به صورت {signal.upper()}")
            try:
                tx_hash = open_position(token, signal)
                print(f"✅ پوزیشن واقعی ثبت شد، TX Hash: {tx_hash}")
            except Exception as e:
                print(f"❌ خطا در باز کردن پوزیشن: {e}")
        else:
            print(f"🔍 هیچ سیگنالی برای {token.upper()} صادر نشده.")

    print("\n⏳ منتظر اجرای بعدی در ۵ دقیقه...\n")
    time.sleep(300)