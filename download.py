#!/usr/bin/env python3
import requests
from clint.textui import progress
import os

url1 = "https://www.tipos.sk/Documents/Csv/loto1.csv"
url2 = "https://www.tipos.sk/Documents/Csv/loto2.csv"

def download (url):
    r = requests.get (url, stream = True)
    file = os.path.basename (url)
    with open (file, "wb") as file:
        total_length = int (r.headers.get ('content-length'))
        for ch in progress.bar (r.iter_content (chunk_size = 2391975), expected_size = (total_length / 1024) + 1):
            if ch:
                file.write (ch)

download (url1)
download (url2)
