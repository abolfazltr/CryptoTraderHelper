import time
from utils.price import get_ohlcv
from utils.strategy import generate_signal
from utils.gmx_v2 import open_position  # اتصال به نسخه واقعی V2

def run_bot():
    print("ربات تریدر GMX V2 استارت شد...\n")
    while True:
        try:
            print("در حال دریافت قیمت جدید...")
            df = get_ohlcv()
            print("دیتای دریافت‌شده:")
            print(df.tail())

            signal = generate_signal(df)
            print("سیگنال تولید شده:", signal)

            if signal in ['buy', 'sell']:
                print(f"در حال باز کردن پوزیشن: {signal}")
                open_position(signal)
            else:
                print("فعلاً سیگنالی برای ورود وجود ندارد.")

        except Exception as e:
            print(f"خطا در اجرای ربات: {e}")

        print("منتظر ۵ دقیقه بعدی...\n")
        time.sleep(300)

if __name__ == "__main__":
    run_bot()