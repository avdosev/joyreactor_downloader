from itertools import chain
from sqlite3 import Connection

def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    key TEXT UNIQUE
    );
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS posts2tags (
    postid INTEGER,
    tagid INTEGER,
    UNIQUE(postid, tagid) ON CONFLICT IGNORE
    );
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS post_images (
    id INTEGER PRIMARY KEY,
    postid INTEGER,
    key TEXT,
    UNIQUE(postid, key) ON CONFLICT IGNORE
    );
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    namel TEXT
    );
    """)
    conn.commit()

def insert_tags(tags, conn: Connection):
    cur = conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO tags (id, name, namel) VALUES(?, ?, ?);", tags)
    conn.commit()

def insert_posts(posts, conn):
    cur = conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO posts (id, key) VALUES(?, ?);", posts)
    conn.commit()

def insert_post_images(images, conn):
    cur = conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO post_images (id, postid, key) VALUES(?, (SELECT id from posts WHERE posts.key = ?), ?);", images)
    conn.commit()

def insert_post2tag(post2tags, conn):
    cur = conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO posts2tags (postid, tagid) VALUES((SELECT id from posts WHERE posts.key = ?), (SELECT id from tags  WHERE tags.name = ?));", post2tags)
    conn.commit()

def select_tags(conn):
    cur = conn.cursor()
    sqlite_select_query = """SELECT * from tags"""
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    return records

def select_posts(conn):
    cur = conn.cursor()
    sqlite_select_query = """SELECT * from posts"""
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    return records

def select_posts2tags(conn):
    cur = conn.cursor()
    sqlite_select_query = """SELECT * from posts2tags"""
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    return records


def insert_info(rx, conn):
    tags = [post['tags'] for post in rx['posts']]
    tagsIds = set(chain.from_iterable(tags))
    tags = [(None, tag, tag.lower()) for tag in tagsIds]
    insert_tags(tags, conn)
    posts = [(None, post['id']) for post in rx['posts']]
    insert_posts(posts, conn)
    posts2tag = list(chain.from_iterable([(post['id'], tag) for tag in post['tags']] for post in rx['posts']))
    insert_post2tag(posts2tag, conn)
    post_images = list(chain.from_iterable([(None, post['id'], imageId) for imageId in post['images']] for post in rx['posts']))
    insert_post_images(post_images, conn)


    