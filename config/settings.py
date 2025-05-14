import os

# خواندن مقادیر از Secrets
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# تنظیمات ثابت ترید
AMOUNT_IN_USD = 20  # مقدار سرمایه به دلار
LEVERAGE = 5        # اهرم استفاده شده