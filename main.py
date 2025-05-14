from utils.strategy import generate_signal
from utils.gmx import open_position
import time

last_signal = None

while True:
    try:
        signal = generate_signal()
        print("سیگنال فعلی:", signal)

        if signal in ["long", "short"] and signal != last_signal:
            open_position(signal)
            last_signal = signal
        else:
            print("پوزیشن قبلاً باز شده یا سیگنال معتبر نیست.")

    except Exception as e:
        print("خطا:", str(e))

    time.sleep(300)  # هر ۵ دقیقه اجرا