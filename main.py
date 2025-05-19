import time

def main():
    print("ربات روشن شد")

    try:
        while True:
            print("وارد حلقه شدیم")
            time.sleep(10)
    except Exception as e:
        print("خطا:", str(e))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("خطای بیرونی:", str(e))