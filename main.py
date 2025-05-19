import time

def main():
    print("ربات روشن شد")

    try:
        while True:
            print("وارد حلقه شدیم")
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write("وارد حلقه شدیم\n")
            time.sleep(10)
    except Exception as e:
        print("خطا:", str(e))
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"خطا: {str(e)}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("خطای بیرونی:", str(e))
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"خطای بیرونی: {str(e)}\n")