import requests
import schedule
import time

def check_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{url} is up.")
        else:
            print(f"{url} is down !!!")
    except requests.ConnectionError:
        print(f"{url} is down !!!")

def job():
    check_website('https://www.example.com')  # Enter your website url

# check the website every 10 minutes
schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)