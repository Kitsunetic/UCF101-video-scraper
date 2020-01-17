import argparse
import collections
import itertools
import os
import re
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

DOWNLOAD_PATH = './download'

def now() -> str:
  return datetime.now().strftime('%H:%M:%S')

def download_video(link: str, fpath: str) -> int:
  with requests.get(link) as resp:
    with open(fpath, 'wb') as f:
      f.write(resp.content)
    return len(resp.content)

def main():
  # Getting list of UCF-101 video data
  URL_UCF101_VIDEOS = 'https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/'
  URL_UCF101_CLASS_LIST = 'http://crcv.ucf.edu/THUMOS14/Class%20Index.txt'
  BASE_URL = 'https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/'

  print('[{}] Reading video list...'.format(now()))
  with requests.get(URL_UCF101_VIDEOS) as resp:
    soup = BeautifulSoup(resp.text, 'lxml')
    links = soup.select_one('table')
    links = soup.select('tr')[3:-1]
    links = map(lambda x: BASE_URL + x.select_one('a')['href'], links)
  
  # Download each videos
  for i, link in enumerate(links):
    # find video path
    name = os.path.basename(link)
    label = re.search('v_(.+?)_.+', name).group(1)
    dir_path = os.path.join(DOWNLOAD_PATH, label)
    file_path = os.path.join(dir_path, name)
    
    # make directory
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)
    
    # download video
    if os.path.exists(file_path):
      # don't download that already downloaded
      print('[{}] {} already exist.'.format(now(), name))
    else:
      print('[{}] Download [{:5}] - {}'.format(now(), i, name))
      download_video(link, file_path)

if __name__ == '__main__':
  main()
