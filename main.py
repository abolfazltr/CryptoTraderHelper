import time
from utils.strategy import get_signal
from utils.gmx_v2 import open_position

# توکن‌هایی که ربات بررسی می‌کنه
TOKENS = ["ETH", "LINK"]

# تابع اصلی ربات
def run_bot():
    print("✅ ربات تریدر شروع شد...\n")

    while True:
        for token in TOKENS:
            print(f"-----------------------------")
            print(f"🔍 بررسی توکن: {token}")
            signal = get_signal(token)

            print(f"📊 سیگنال دریافتی برای {token}: {signal}")

            if signal == "buy":
                print(f"✅ سیگنال خرید برای {token} تأیید شد.")
                open_position(token_symbol=token, is_long=True)
            elif signal == "sell":
                print(f"✅ سیگنال فروش برای {token} تأیید شد.")
                open_position(token_symbol=token, is_long=False)
            else:
                print(f"❌ هیچ سیگنال معتبری برای {token} صادر نشد.")

        print("⏱️ منتظر ۵ دقیقه بعدی...\n")
        time.sleep(300)

# اجرای ربات
run_bot()