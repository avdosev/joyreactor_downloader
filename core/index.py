from sqlite3 import Connection
import sqlite3
from find_lang import *
from parser.db import *

def gen_sql_from_ast(ast, depth=1):
    values = []
    for element in ast:
        t = element['type']
        if t == 'text':
            values.append(f"select DISTINCT posts2tags.postid from posts2tags, tags where instr(tags.namel, \"{element['value']}\") AND tags.id = posts2tags.tagid\n")
        elif t == 'op':
            if element['op'] == 'and':
                values.append(f"INTERSECT\n")
            elif element['op'] == 'or':
                values.append(f"UNION\n")
        elif t == 'combine':
            r = gen_sql_from_ast(element['values'], depth=depth+1)
            if r == '': break
            values.append(f'select * from (\n{r})\n')
    
    return ''.join(map(lambda s: ' '*depth + s, values))

def gen_sql(s):
    terms = extract_terms(s)
    elements = prepare_terms(terms)
    print(elements)
    ast = make_ast(elements)
    pprint(ast)

    return gen_sql_from_ast(ast)

def find(s, conn: Connection):
    sql = gen_sql(s)
    req = f'SELECT posts.key FROM posts, (\n{sql}) as postsIds where posts.id=postsIds.postid;'
    print(req)
    cur = conn.cursor()
    cur.execute(req)
    records = cur.fetchall()
    return records
    


if __name__ == '__main__':
    # sql_request = gen_sql("anime (ero | porn) ino kek puk")
    home = '..'
    db = sqlite3.connect(f'{home}/data.db')
    print(select_tags(db))
    print(select_posts2tags(db))
    records = find("anime yuki", db)
    print(records)