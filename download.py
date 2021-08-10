#!/usr/bin/env python3
import requests
from clint.textui import progress
import os

url1 = "https://www.tipos.sk/loterie/ciselne-loterie/archiv-vyzrebovanych-cisel?file=loto1"
url2 = "https://www.tipos.sk/loterie/ciselne-loterie/archiv-vyzrebovanych-cisel?file=loto2"

def download (url, file):
    r = requests.get (url, stream = True)
    if r.status_code == 200:
        with open (file, "wb") as file:
            total_length = int (r.headers.get ('content-length'))
            for ch in progress.bar (r.iter_content (chunk_size = 2391975), expected_size = (total_length / 1024) + 1):
                if ch:
                    file.write (ch)
    else:
        print("Download failed", r.status_code)

download (url1, "loto1.csv")
download (url2, "loto2.csv")
