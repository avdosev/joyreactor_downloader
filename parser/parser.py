import json
from pprint import pprint
from parse import *
import sqlite3
from db import *
home = '..'
with open(f'{home}/config.json') as f:
    config = json.load(f)

db = sqlite3.connect(f'{home}/data.db')
create_tables(db)

result = get_tag_page('Anime', page=1)
rx = extract_main_info(result)
insert_info(rx, db)