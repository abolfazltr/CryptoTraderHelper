import time
import logging
from utils.price import get_last_prices, get_price_from_coingecko
from utils.strategy import get_signal
from config.tokens import TOKENS
from utils.gmx_v2 import open_position  # ← این مسیر همون بمونه

logging.basicConfig(level=logging.INFO)

def analyze_token(token):
    print(f"\n[{token['symbol']}] تحلیل در حال اجرا...")

    # دریافت لیست قیمت واقعی
    prices = get_last_prices(token['symbol'])

    if not prices or len(prices) < 20:
        print("قیمت کافی برای تحلیل وجود ندارد.")
        return

    # تحلیل
    result = get_signal(token["symbol"], prices[-1])  # قیمت آخر (کندل جدیدترین)
    logging.info(f"[DEBUG] نتایج تحلیل برای {token['symbol']}: {result}")

    print(f"Supertrend: {result['supertrend']}")
    print(f"EMA short: {result['ema_short']} | EMA long: {result['ema_long']}")

    if result['ema_cross']:
        print("کراس EMA برقرار است.")
    else:
        print("کراس EMA برقرار نیست.")

    if result['signal'] == "long":
        print("سیگنال نهایی: پوزیشن LONG → وارد شو")
        open_position("long", token["symbol"])
    elif result['signal'] == "short":
        print("سیگنال نهایی: پوزیشن SHORT → وارد شو")
        open_position("short", token["symbol"])
    else:
        print("سیگنال نهایی: ورود نکن")

# اجرای مداوم هر ۵ دقیقه
while True:
    print("=" * 60)
    for token in TOKENS:
        analyze_token(token)

    print("\nدر حال انتظار برای دور بعدی...\n")
    time.sleep(300)