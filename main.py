from datetime import datetime
import time
from utils.strategy import generate_signal
from utils.gmx import open_position

while True:
    try:
        print("\n[", datetime.now(), "] Checking for signal...")
        signal = generate_signal()
        print("Signal:", signal)

        if signal in ["long", "short"]:
            print("Opening position for:", signal)
            open_position(signal, leverage=5, amount_usd=20, token="WETH")
        else:
            print("No valid signal found.")

    except Exception as e:
        print("خطا:", str(e))

    print("Waiting 5 minutes...")
    time.sleep(300)