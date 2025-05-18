import time
from utils.strategy import generate_signal
from utils.gmx import open_position

while True:
    try:
        signal = generate_signal()
        print("Signal:", signal)

        if signal in ["long", "short"]:
            print("Opening position for:", signal)
            open_position(signal)
        else:
            print("No valid signal found.")

    except Exception as e:
        print("خطا:", str(e))

    time.sleep(300)
    print("Waiting 5 minutes...")