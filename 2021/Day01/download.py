import requests


url = f'https://adventofcode.com/2021/day/1/input'
r = requests.get(url, allow_redirects=True)

open('input.txt', 'wb').write(r.content)