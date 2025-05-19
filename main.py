import time
import pandas as pd
from utils.price import get_current_price
from utils.strategy import generate_signal
from utils.gmx_v2 import open_position

def run_bot():
    print("✅ ربات تریدر GMX V2 با موفقیت استارت شد...\n", flush=True)

    while True:
        try:
            print("⏳ در حال دریافت قیمت لحظه‌ای ETH از GMX...", flush=True)
            price = get_current_price()

            if price is None:
                print("⚠️ دریافت قیمت ناموفق بود. تلاش مجدد در ۵ دقیقه...", flush=True)
            else:
                print(f"✅ قیمت فعلی ETH از GMX: {price} دلار", flush=True)

                # ساخت دیتافریم برای تحلیل
                df = pd.DataFrame({
                    'close': [price] * 30,
                    'high': [price] * 30,
                    'low': [price] * 30
                })

                signal = generate_signal(df)
                print(f"🔍 سیگنال تولید شده: {signal}", flush=True)

                if signal in ['buy', 'sell']:
                    print(f"✅ در حال باز کردن پوزیشن واقعی: {signal}", flush=True)
                    open_position(signal)
                else:
                    print("❌ هیچ سیگنالی برای ورود وجود ندارد.", flush=True)

        except Exception as e:
            print(f"🚨 خطا در اجرای ربات: {e}", flush=True)

        print("🕒 منتظر ۵ دقیقه بعدی...\n", flush=True)
        time.sleep(300)

if __name__ == "__main__":
    run_bot()