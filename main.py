import time
from utils.price import get_ohlcv
from utils.strategy import generate_signal
from utils.gmx import open_position

def run_bot():
    while True:
        print("شروع بررسی کندل جدید...\n")
        try:
            df = get_ohlcv()
            print("داده‌های قیمت:", df)

            signal = generate_signal(df)
            print("سیگنال تولید شده:", signal)

            if signal in ['buy', 'sell']:
                print(f"سیگنال دریافت شد: {signal}")
                open_position(signal)
            else:
                print("هیچ سیگنالی برای ورود وجود ندارد.")

        except Exception as e:
            print(f"خطا در اجرای ربات: {e}")

        print("در حال انتظار برای ۵ دقیقه بعدی...\n")
        time.sleep(300)

if __name__ == "__main__":
    run_bot()