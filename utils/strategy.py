import requests

def generate_signal():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "ETHUSDT",
        "interval": "5m",
        "limit": 50
    }
    response = requests.get(url, params=params)
    data = response.json()

    closes = [float(candle[4]) for candle in data if len(candle) > 4]

    if len(closes) < 21:
        return "none"

    ema9 = sum(closes[-9:]) / 9
    ema21 = sum(closes[-21:]) / 21

    rsi_period = 14
    gains, losses = [], []
    for i in range(1, rsi_period + 1):
        diff = closes[-i] - closes[-i - 1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = sum(gains) / rsi_period
    avg_loss = sum(losses) / rsi_period if losses else 1
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    if ema9 > ema21 and rsi < 70:
        return "long"
    elif ema9 < ema21 and rsi > 30:
        return "short"
    else:
        return "none"