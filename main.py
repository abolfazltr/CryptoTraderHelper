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

        price = get_current_price(token)
        if price is None:
            print(f"❌ دریافت قیمت برای {token.upper()} با خطا مواجه شد.")
            sys.stdout.flush()
            continue

        print(f"✅ قیمت فعلی {token.upper()}: {price}")
        sys.stdout.flush()

        print("🔍 تحلیل تکنیکال در حال انجام است...")
        sys.stdout.flush()

        signal = analyze_token(token)

        if signal is None:
            print(f"❌ سیگنال None برگشت داده شده برای {token.upper()} — احتمالاً خطا در دیتا یا تحلیل")
            sys.stdout.flush()
            continue

        print(f"📈 وضعیت Supertrend: {signal['supertrend']}")
        print(f"📊 EMA short: {signal['ema_short']} | EMA long: {signal['ema_long']}")
        print(f"🔎 EMA signal: {signal['ema_signal']}")
        sys.stdout.flush()

        if signal["final_signal"] is None:
            print(f"❌ هیچ سیگنال معتبری صادر نشد برای {token.upper()}.\n")
        else:
            print(f"✅ سیگنال نهایی برای {token.upper()}: {signal['final_signal']}")
            print(f"🚀 تلاش برای باز کردن پوزیشن واقعی...")
            sys.stdout.flush()

            try:
                tx_hash = open_position(token, signal['final_signal'])
                print(f"📬 تراکنش ارسال شد: {tx_hash}")
            except Exception as e:
                print(f"❌ خطا در ارسال تراکنش: {e}")
            sys.stdout.flush()

        print("--------------------------------------------------")
        sys.stdout.flush()

    print("⏳ منتظر اجرای بعدی در ۵ دقیقه...\n")
    sys.stdout.flush()
    time.sleep(300)