from utils.price import get_ohlcv
from utils.strategy import generate_signal
from utils.gmx import open_position

df = get_ohlcv()
signal = generate_signal(df)

if signal in ['long', 'short']:
    open_position(signal)
else:
    print("No signal detected.")