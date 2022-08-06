import json
from pprint import pprint
from parse import *
import sqlite3
from db import *
home = '../..'

with open(f'{home}/config.json') as f:
    config = json.load(f)
with open(f'{home}/parser_state.json') as f:
    state = json.load(f)

db = sqlite3.connect(f'{home}/data.db')
create_tables(db)

latest_tag = state['tag'] if 'tag' in state else None 
latest_tag_index = config['tags'].index(latest_tag)
start_index = latest_tag_index+1

for tag in config['tags'][start_index:]:
    state['tag'] = tag
    
    page = 1
    limit = 2
    while page < limit:
        print(f'tag:{tag} page:{page} limit:{limit}')
        result = get_tag_page(tag, page=page)
        print('end')
        rx = extract_main_info(result)
        insert_info(rx, db)
        limit = rx['pages']
        page += 1
    with open(f'{home}/parser_state.json', 'w') as f:
        json.dump(state, f)