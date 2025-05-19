import time
from utils.price import get_ohlcv
from utils.strategy import generate_signal
from utils.gmx import open_position

def run_bot():
    while True:
        print("در حال دریافت داده جدید...")
        try:
            df = get_ohlcv()
            signal = generate_signal(df)

            if signal in ['buy', 'sell']:
                print(f"سیگنال دریافت شد: {signal}")
                open_position(signal)
            else:
                print("سیگنالی دریافت نشد.")

        except Exception as e:
            print(f"خطا در اجرای ربات: {e}")

        print("منتظر ۵ دقیقه بعدی...\n")
        time.sleep(300)  # 300 ثانیه = 5 دقیقه

if __name__ == "__main__":
    run_bot()