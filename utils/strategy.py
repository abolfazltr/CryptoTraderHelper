from utils.indicators import calculate_supertrend, calculate_ema
from utils.price import get_last_prices

def get_signal(symbol, current_price):
    try:
        prices = get_last_prices(symbol)
        print(f"[DEBUG] قیمت‌های دریافت‌شده برای {symbol}: {prices}")

        if len(prices) < 20:
            print(f"[ERROR] تعداد قیمت کافی نیست برای {symbol}")
            return {"signal": None, "supertrend": "UNKNOWN", "ema_short": 0, "ema_long": 0, "ema_cross": False}

        ema_short = calculate_ema(prices, period=10)[-1]
        ema_long = calculate_ema(prices, period=20)[-1]
        ema_cross = ema_short > ema_long

        supertrend_list = calculate_supertrend(prices, period=10, multiplier=2)
        trend = supertrend_list[-1] if supertrend_list else "unknown"

        signal = None
        if trend == "up" and ema_cross:
            signal = "long"
        elif trend == "down" and ema_cross:
            signal = "short"

        return {
            "supertrend": "LONG" if trend == "up" else "SHORT",
            "ema_short": round(ema_short, 2),
            "ema_long": round(ema_long, 2),
            "ema_cross": ema_cross,
            "signal": signal
        }

    except Exception as e:
        print("[EXCEPTION]", e)
        return {"signal": None, "supertrend": "ERROR", "ema_short": 0, "ema_long": 0, "ema_cross": False}