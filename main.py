import time
from utils.price import get_current_price
from utils.strategy import generate_signal
from utils.gmx_v2 import open_position
import pandas as pd

def run_bot():
    print("استارت شد ربات تریدر GMX V2 ...\n")

    while True:
        try:
            print("در حال دریافت قیمت لحظه‌ای ETH از GMX...")
            price = get_current_price()

            if price is None:
                print("⚠️  قیمت دریافت نشد، منتظر تلاش بعدی می‌مانیم...\n")
            else:
                print(f"✅ قیمت فعلی ETH: {price} دلار")

                # ساخت دیتافریم برای تحلیل
                df = pd.DataFrame({
                    'close': [price] * 30  # فرض می‌گیریم ۳۰ کندل داریم با همین قیمت
                })

                signal = generate_signal(df)
                print("سیگنال تولید شده:", signal)

                if signal in ['buy', 'sell']:
                    print(f"در حال باز کردن پوزیشن واقعی: {signal}")
                    open_position(signal)
                else:
                    print("❌ هیچ سیگنالی برقرار نیست. برای ورود وجود ندارد.")

        except Exception as e:
            print(f"خطا در اجرای ربات: {e}")

        print("⏰ منتظر ۵ دقیقه بعدی...\n")
        time.sleep(300)

if __name__ == "__main__":
    run_bot()