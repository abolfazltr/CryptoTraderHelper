import time

def main():
    print("ربات روشن شد")  # تست: آیا وارد تابع main میشه یا نه

    while True:
        print("وارد حلقه شدیم")  # تست: آیا وارد حلقه میشه یا نه
        time.sleep(10)  # هر ۱۰ ثانیه چاپ کنه

if __name__ == "__main__":
    main()