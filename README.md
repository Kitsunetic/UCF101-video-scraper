# Download UCF-101 videos

Download `UCF-101` videos.

Referenced video data from here

- https://www.crcv.ucf.edu/data/UCF101.php
- http://www.thumos.info/download.html
- https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/

## Requirements

Check [requirements.txt](./requirements.txt)

- Python 3
- requests
- bs4

```bash
sudo pip3 install requests bs4
```

## Usage

```bash
git clone https://github.com/Kitsunetic/download-ucf101-videos
pip3 install -r requirements.txt
python3 download_ucf101_dataset.py
```

## Download Path

You can specify download path by editing [download_ucf101_dataset.py](./download_ucf101_dataset.py)
Change global variable `DOWNLOAD_PATH` into what you want to download videos files.

```python
DOWNLOAD_PATH = '{directory path to download video files}'
```
