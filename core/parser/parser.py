import json
from pprint import pprint
import time
from parse import *
import sqlite3
from db import *
home = '../..'
state = {}

def flush_state():
    global state
    with open(f'{home}/parser_state.json', 'w', encoding='utf-8') as f:
            json.dump(state, f)

def flush_json(j):
    with open(f'{home}/json.json', 'w', encoding='utf-8') as f:
            json.dump(j, f, ensure_ascii=False, indent=2)

def main():
    global state

    with open(f'{home}/config.json', encoding='utf-8') as f:
        config = json.load(f)
    with open(f'{home}/parser_state.json', encoding='utf-8') as f:
        state = json.load(f)

    db = sqlite3.connect(f'{home}/data.db')
    create_tables(db)

    latest_tag = state['tag'] if 'tag' in state else None 
    try:
        latest_tag_index = config['tags'].index(latest_tag)
    except ValueError:
        latest_tag_index = -1
    start_index = latest_tag_index+1

    for tag in config['tags'][start_index:]:
        state['tag'] = tag
        
        page = 1
        limit = 2
        while page < limit:
            print(f'tag:{tag} page:{page} limit:{limit}')
            try:
                result = get_tag_page(tag, page=page)
                flush_json(result)
            except:
                print('stoped on', page, 'page with limit', limit)
                flush_state()
                return
            print('end')
            rx = extract_main_info(result)
            insert_info(rx, db)
            limit = rx['pages']
            page += 1
            time.sleep(1.5)
        flush_state()

if __name__ == '__main__':
    main()