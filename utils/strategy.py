def get_signal(token):
    print(f"در حال بررسی شرایط برای {token}...")

    # شبیه‌سازی داده‌ها (در نسخه نهایی با دیتا واقعی جایگزین کن)
    supertrend_signal = "LONG"
    ema_short = 2479.77
    ema_long = 2479.77

    print(f"supertrend: {supertrend_signal}")
    print(f"EMA short: {ema_short} | EMA long: {ema_long}")
    print(f"EMA cross condition: {ema_short} → {ema_long}")

    if supertrend_signal == "LONG" and ema_short > ema_long:
        print("سیگنال خرید تولید شد 🔍")
        return "buy"
    elif supertrend_signal == "SHORT" and ema_short < ema_long:
        print("سیگنال فروش تولید شد 🔍")
        return "sell"
    else:
        print("❌ هیچ شرایط سیگنالی برقرار نیست.")
        return None