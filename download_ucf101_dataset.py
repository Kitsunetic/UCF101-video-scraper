import argparse
import collections
import itertools
import os
import re
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

DOWNLOAD_PATH = "./download"

def now():
    return datetime.now().strftime("%H:%M:%S")

def download(start=0, end=-1) -> None:
    # Getting list of UCF-101 video data
    URL_UCF101_VIDEOS = "https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/"
    URL_UCF101_CLASS_LIST = "http://crcv.ucf.edu/THUMOS14/Class%20Index.txt"
    BASE_URL = "https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/"

    print("[{}] Reading video list...".format(now()))
    with requests.get(URL_UCF101_VIDEOS) as resp:
        soup = BeautifulSoup(resp.text, "lxml")
        links = soup.select_one("table")
        links = soup.select("tr")[3:-1]
        links = map(lambda x: BASE_URL + x.select_one("a")["href"], links)
        links = itertools.islice(links, start, end if end >= 0 else None)
        # links example... contains 13320 videos
        # https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/v_ApplyEyeMakeup_g01_c01.avi
        # https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/v_ApplyEyeMakeup_g01_c02.avi
        # https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/v_ApplyEyeMakeup_g01_c03.avi
        # https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/v_ApplyEyeMakeup_g01_c04.avi
        # https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/v_ApplyEyeMakeup_g01_c05.avi
        # https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/v_ApplyEyeMakeup_g01_c06.avi
        # https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/v_ApplyEyeMakeup_g02_c01.avi
        # https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/v_ApplyEyeMakeup_g02_c02.avi
    
    # Download each videos
    for i, link in enumerate(links, start):
        basename = os.path.basename(link)
        label = re.search("v_(.+?)_.+", basename).group(1)
        dpath = os.path.join(DOWNLOAD_PATH, label)
        fpath = os.path.join(dpath, basename)
        
        if not os.path.exists(dpath):
            os.makedirs(dpath)
            
        if os.path.exists(fpath):
            print("[{}] Already exist [{:5}] - {}".format(now(), i, basename))
            continue
        
        print("[{}] Download [{:5}] - {}".format(now(), i, basename))
        try:
            with requests.get(link) as resp:
                with open(fpath, "wb") as f:
                    f.write(resp.content)
        except:
            print("[{}] [ERROR!] Cannot download [{:5}] - {}".format(now(), i, basename))

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", "-s", type=int, default=0, help="start index")
    parser.add_argument("--end", "-e", type=int, default=-1, help="end index")
    p = parser.parse_args(sys.argv[1:])
    
    download(p.start, p.end)

if __name__ == "__main__":
    main()
