import time
from utils.price import get_ohlcv
from utils.strategy import generate_signal
from utils.gmx_v2 import open_position  # استفاده از فایل جدید

def run_bot():
    print("ربات تریدر GMX V2 استارت شد...\n")
    while True:
        try:
            print("در حال دریافت قیمت کندل جدید...")
            df = get_ohlcv()
            print("دیتای دریافت‌شده:")
            print(df.tail())

            signal = generate_signal(df)
            print("سیگنال تولید شده:", signal)

            if signal in ['buy', 'sell']:
                print(f"سیگنال تأیید شده: {signal} → در حال باز کردن پوزیشن...")
                open_position(signal)
            else:
                print("سیگنالی برای ورود وجود ندارد.")

        except Exception as e:
            print(f"خطا در اجرای ربات: {e}")

        print("در حال انتظار برای ۵ دقیقه بعدی...\n")
        time.sleep(300)  # 5 دقیقه


if __name__ == "__main__":
    run_bot()