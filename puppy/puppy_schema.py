from sqlalchemy import Table, Column, String, DDL, event, Integer, Boolean, TIMESTAMP, ForeignKey, UniqueConstraint
from puppy.database import db_metadata


event.listen(db_metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS puppy"))

user_table = Table(
    'user', db_metadata,
    Column('username', String(32), primary_key=True),
    Column('password_hash', String(64), nullable=False),
    Column('salt', String(24), nullable=False),
    Column('site_admin', Boolean, nullable=False, server_default='FALSE'),
    schema='puppy'
)

post_table = Table(
    'post', db_metadata,
    Column('id', Integer, primary_key=True),
    Column('user', String(32), ForeignKey('puppy.user.username')),
    Column('content', String(255), nullable=False),  # 255 character limit!? Take that Twitter!
    Column('timestamp', TIMESTAMP, nullable=False),
    schema='puppy'
)

post_favorite_table = Table(
    'post_favorite', db_metadata,
    Column('post_id', Integer, ForeignKey('puppy.post.id'), nullable=False),
    Column('user', String(32), ForeignKey('puppy.user.username'), nullable=False),
    UniqueConstraint('post_id', 'user'),
    schema='puppy'
)
