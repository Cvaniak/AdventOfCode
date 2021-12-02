from datetime import datetime
from download import download_input
import requests
import shutil
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) == 2:
        day = int(sys.argv[1])
    else:
        day = datetime.today().day

    root = os.path.abspath(os.getcwd())
    template = os.path.join(root, "2021/template")
    new_day = os.path.join(root, f"2021/Day{day:02d}")

    try:
        shutil.copytree(template, new_day)
    except Exception as e:
        ...
    
    download_input(day)
    print(new_day)
