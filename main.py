import time
import logging
from utils.price import get_price_from_gmx, get_price_from_coingecko
from utils.strategy import get_signal
from config.tokens import TOKENS
from utils.gmx_v2 import open_position  # ← مسیر اصلاح‌شده

# تنظیم لاگر
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def analyze_token(token):
    logging.info(f"[{token['symbol']}] تحلیل در حال اجرا...")

    price_gmx = get_price_from_gmx(token['gmx_id'])
    price_cg = get_price_from_coingecko(token['coingecko_id'])
    final_price = price_gmx if price_gmx else price_cg

    if not final_price:
        logging.warning("قیمت نهایی یافت نشد. تحلیل انجام نشد.")
        return

    logging.info(f"قیمت از GMX: {price_gmx}")
    logging.info(f"قیمت از CoinGecko: {price_cg}")
    logging.info(f"قیمت نهایی: {final_price}")

    result = get_signal(token["symbol"], final_price)
    logging.debug(f"[DEBUG] قیمت‌های دریافت‌شده برای {token['symbol']}: {result}")

    logging.info(f"Supertrend: {result['supertrend']}")
    logging.info(f"EMA short: {result['ema_short']} | EMA long: {result['ema_long']}")

    if result['ema_cross']:
        logging.info("کراس EMA برقرار است.")
    else:
        logging.info("کراس EMA برقرار نیست.")

    if result['signal'] == "long":
        logging.info("سیگنال نهایی: پوزیشن LONG → وارد شو")
        open_position("long", token["symbol"])
    elif result['signal'] == "short":
        logging.info("سیگنال نهایی: پوزیشن SHORT → وارد شو")
        open_position("short", token["symbol"])
    else:
        logging.info("سیگنال نهایی: ورود نکن")

# اجرای مداوم هر ۵ دقیقه
if __name__ == "__main__":
    while True:
        logging.info("=" * 60)
        for token in TOKENS:
            analyze_token(token)
        logging.info("در حال انتظار برای دور بعدی...\n")
        time.sleep(300)