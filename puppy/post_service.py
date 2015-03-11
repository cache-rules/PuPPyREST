from datetime import datetime
from sqlalchemy import select, desc
from sqlalchemy import func

from puppy.puppy_schema import post_table, post_favorite_table
import puppy.database as database


_pc = post_table.c
_fc = post_favorite_table.c
posts_query = select([_pc.id, _pc.user, _pc.content, _pc.timestamp, func.count(_fc.post_id).label('fav_count')])
posts_query = posts_query.select_from(post_table.outerjoin(post_favorite_table))
posts_query = posts_query.order_by(desc(_pc.timestamp))
posts_query = posts_query.group_by(_pc.id)


def get_posts():
    with database.db_engine.begin() as conn:
        rows = conn.execute(posts_query).fetchall()

    posts = []

    for row in rows:
        posts.append({'id': row['id'], 'username': row['user'], 'content': row['content'],
                      'timestamp': row['timestamp'].timestamp(), 'fav_count': row['fav_count']})

    return posts


def get_post(post_id):
    with database.db_engine.begin() as conn:
        result = conn.execute(posts_query.where(post_table.c.id == post_id)).fetchone()

    return {'id': result['id'], 'username': result['user'], 'content': result['content'],
            'timestamp': result['timestamp'].timestamp(), 'fav_count': result['fav_count']}


def add_post(username, content):
    with database.db_engine.begin() as conn:
        values = {'user': username, 'content': content, 'timestamp': datetime.now()}
        result = conn.execute(post_table.insert(values=values)).inserted_primary_key[0]

    return get_post(result)


def delete_post(post_id):
    with database.db_engine.begin() as conn:
        conn.execute(post_favorite_table.delete().where(post_favorite_table.c.post_id == post_id))
        conn.execute(post_table.delete().where(post_table.c.id == post_id))

    return {'success': True}


def add_favorite(username, post_id):
    with database.db_engine.begin() as conn:
        values = {'post_id': post_id, 'user': username}
        conn.execute(post_favorite_table.insert(values=values))

    return {'success': True}


def get_favorites(post_id):
    with database.db_engine.begin() as conn:
        result = conn.execute(post_favorite_table.select().where(post_favorite_table.c.post_id == post_id)).fetchall()

    favs = []

    for row in result:
        favs.append({'post_id': row['post_id'], 'user': row['user']})

    return favs
