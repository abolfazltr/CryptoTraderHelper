import time
from utils.price import get_token_price
from utils.strategy import generate_signal
from utils.gmx import open_position

# تنظیمات توکن‌ها
TOKENS = {
    "ETH": {"amount_usd": 20},
    "LINK": {"amount_usd": 20}
}

# درصد سود و ضرر
TP_PERCENT = 0.04  # ۴٪ سود
SL_PERCENT = 0.025  # ۲.۵٪ ضرر

# حلقه اصلی ربات
while True:
    for token in TOKENS:
        print(f"\nبررسی توکن: {token}")

        price = get_token_price(token)
        print("قیمت لحظه‌ای:", price)

        signal = generate_signal(token)
        print("سیگنال تحلیل:", signal)

        if signal in ["LONG", "SHORT"]:
            is_long = signal == "LONG"
            entry_price = price

            # محاسبه حد سود و ضرر
            if is_long:
                tp_price = entry_price * (1 + TP_PERCENT)
                sl_price = entry_price * (1 - SL_PERCENT)
            else:
                tp_price = entry_price * (1 - TP_PERCENT)
                sl_price = entry_price * (1 + SL_PERCENT)

            print(f"باز کردن پوزیشن {signal} روی {token}...")
            print(f"Entry: {entry_price:.2f}, TP: {tp_price:.2f}, SL: {sl_price:.2f}")

            open_position(
                token_symbol=token,
                is_long=is_long,
                amount_usd=TOKENS[token]["amount_usd"],
                entry_price=entry_price,
                tp_price=tp_price,
                sl_price=sl_price
            )
        else:
            print("سیگنال معتبری نیست. فعلاً پوزیشنی باز نمی‌شود.")

    # صبر ۵ دقیقه‌ای
    time.sleep(300)