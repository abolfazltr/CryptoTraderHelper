import time
from utils.strategy import get_signal
from utils.gmx_v2 import open_position

# لیست توکن‌هایی که بررسی می‌شن
TOKENS = ["ETH", "LINK"]

# تابع اصلی اجرا
def run_bot():
    print("✅ ربات تریدر فعال شد و در حال اجراست...\n")

    while True:
        for token in TOKENS:
            print("--------------------------------------------------")
            print(f"🔍 در حال بررسی توکن: {token}")

            signal = get_signal(token)
            print(f"📊 سیگنال دریافتی: {signal}")

            if signal == "buy":
                print(f"✅ سیگنال خرید برای {token} تأیید شد.")
                open_position(token_symbol=token, is_long=True)

            elif signal == "sell":
                print(f"✅ سیگنال فروش برای {token} تأیید شد.")
                open_position(token_symbol=token, is_long=False)

            else:
                print(f"❌ هیچ سیگنالی برای {token} صادر نشد.")

        print("\n⏱️ منتظر ۵ دقیقه بعدی...\n")
        time.sleep(300)


# اجرای خودکار برنامه در Render و Replit
if __name__ == "__main__":
    run_bot()