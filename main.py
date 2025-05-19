import time
from utils.price import get_price_data
from utils.strategy import generate_signal
from utils.gmx import open_position

# تنظیمات پوزیشن
LEVERAGE = 5
AMOUNT_USD = 20
TOKEN = "WETH"

def main():
    print("ربات روشن شد")

    while True:
        try:
            print("در حال بررسی قیمت‌ها...")

            prices = get_price_data("ETHUSDT", "5m", 100)
            print(f"آخرین قیمت‌ها: {prices.tail(1)}")

            signal = generate_signal(prices)
            print(f"سیگنال فعلی: {signal}")

            if signal in ["long", "short"]:
                print(f"سیگنال دریافت شد: {signal}")
                open_position(signal, LEVERAGE, AMOUNT_USD, TOKEN)
            else:
                print("سیگنالی برای ورود وجود ندارد.")
        except Exception as e:
            print("خطا در اجرای ربات:", str(e))

        time.sleep(300)  # هر ۵ دقیقه

if __name__ == "__main__":
    main()