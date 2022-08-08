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
            f.flush()

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
    page = 1 
    try:
        latest_tag_index = config['tags'].index(latest_tag)
        if 'page' in state:
            page = state['page']
    except ValueError:
        latest_tag_index = 0
    start_index = latest_tag_index

    for tag in config['tags'][start_index:]:
        state['tag'] = tag
        limit = None
        
        try:
            while limit is None or page < limit:
                print(f'tag:{tag} page:{page} limit:{limit}')
                result = get_tag_page(tag, page=page)
                flush_json(result)
                print('end')
                rx = extract_main_info(result)
                insert_info(rx, db)
                limit = rx['pages']
                page += 1
                state['page'] = page
                time.sleep(1.5)
            flush_state()
            page = 1
        except KeyboardInterrupt:
            return
        except:
            print('stopped on', page, 'page with limit', limit)
        finally:
            flush_state()

if __name__ == '__main__':
    main()