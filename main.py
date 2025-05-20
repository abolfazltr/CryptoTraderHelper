import time
from utils.price import get_price_from_gmx, get_price_from_coingecko
from utils.strategy import get_signal
from config.tokens import TOKENS
from utils.gmx_v2 import open_position  # ← مسیر اصلاح‌شده

def analyze_token(token):
    print(f"\n[{token['symbol']}] تحلیل در حال اجرا...")

    # دریافت قیمت‌ها
    price_gmx = get_price_from_gmx(token['gmx_id'])
    price_cg = get_price_from_coingecko(token['coingecko_id'])
    final_price = price_gmx if price_gmx else price_cg

    if not final_price:
        print("قیمت نهایی یافت نشد. تحلیل انجام نشد.")
        return

    print(f"قیمت از GMX: {price_gmx}")
    print(f"قیمت از CoinGecko: {price_cg}")
    print(f"قیمت نهایی: {final_price}")

    # تحلیل
    result = get_signal(token["symbol"], final_price)
    print(f"[DEBUG] قیمت‌های دریافت‌شده برای {token['symbol']}: {result}")

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