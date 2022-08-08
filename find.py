import sqlite3
import sys
import os

from core.index import find, find_images
from utils.image_downloader import download_image
from utils.url import gen_url

if __name__ == '__main__':
    home = '.'
    db = sqlite3.connect(f'{home}/data.db')
    if len(sys.argv) >= 3:
        output_dir = sys.argv[2]
        cache_dir = f'{home}/cache'
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(cache_dir, exist_ok=True)
        records = find_images(sys.argv[1], db)
        print('count:', len(records))
        for record in records:
            download_image(record[1], output_dir, cache_dir)
    else:    
        records = find(sys.argv[1], db)
        for record in records:
            key = record[1]
            print(gen_url(key))