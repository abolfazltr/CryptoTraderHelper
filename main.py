import time
import os

def log(text):
    with open("log.txt", "a") as f:
        f.write(text + "\n")

def main():
    log("ربات روشن شد")
    try:
        for i in range(3):  # فقط 3 بار تست کنه
            log(f"وارد حلقه شدیم - مرحله {i+1}")
            time.sleep(5)
    except Exception as e:
        log("خطا: " + str(e))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log("خطای بیرونی: " + str(e))

    # بعد از اجرای ربات، push کنه
    os.system("git config --global user.email 'log@bot.com'")
    os.system("git config --global user.name 'LogBot'")
    os.system("git add log.txt")
    os.system("git commit -m 'log update'")
    os.system("git push")