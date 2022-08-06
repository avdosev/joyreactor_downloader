import sqlite3
import sys

from core.index import find
from utils.url import gen_url

if __name__ == '__main__':
    home = '.'
    db = sqlite3.connect(f'{home}/data.db')
    records = find(sys.argv[1], db)
    for record in records:
        key = record[0]
        print(gen_url(key))