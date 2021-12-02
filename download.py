from datetime import datetime
import requests
import os
from dotenv import load_dotenv

def download_input(day):
    load_dotenv()

    url = f'https://adventofcode.com/2021/day/{day}/input'
    r = requests.get(url, allow_redirects=True, cookies={"session":os.getenv("SESSION")})

    open(f'./2021/Day{day:02d}/input.txt', 'wb').write(r.content)

if __name__ == '__main__':
    day = datetime.today().day
    download_input(day)
