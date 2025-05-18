import time
from utils.strategy import generate_signal
from utils.gmx import open_position

# تنظیمات پوزیشن
LEVERAGE = 5
AMOUNT_USD = 20
TOKEN = "WETH"

def main():
    while True:
        try:
            signal = generate_signal()
            if signal in ["long", "short"]:
                print(f"سیگنال دریافت شد: {signal}")
                open_position(signal, LEVERAGE, AMOUNT_USD, TOKEN)
            else:
                print("سیگنالی برای ورود وجود ندارد.")
        except Exception as e:
            print("خطا در اجرای ربات:", str(e))

        time.sleep(300)  # ۵ دقیقه صبر کن

if __name__ == "__main__":
    main()