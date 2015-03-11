import hashlib
from base64 import b64encode
from os import urandom
from threading import RLock

from puppy.puppy_schema import user_table
import puppy.database as database


_user_cache = {}
_cache_lock = RLock()


def create_salt() -> str:
    # We store the salts as strings, so we just convert it to a string straight away here.
    return b64encode(urandom(16)).decode('utf-8')


def hash_password(password: str, salt: str) -> str:
    sha = hashlib.new('sha256')
    sha.update(salt.encode('utf-8') + password.encode('utf-8'))
    return sha.hexdigest()


def create_user(username, password, site_admin=False):
    print('Creating user with username "{}"'.format(username))
    salt = create_salt()
    pwd_hash = hash_password(password, salt)

    with database.db_engine.begin() as conn:
        values = {'username': username, 'password_hash': pwd_hash, 'salt': salt, 'site_admin': site_admin}
        conn.execute(user_table.insert(values=values))

    return {'username': username, 'site_admin': site_admin}


def retrieve_user(username):
    with database.db_engine.begin() as conn:
        result = conn.execute(user_table.select().where(user_table.c.username == username)).fetchone()

    if len(result) > 0:
        user = {'username': username, 'password_hash': result['password_hash'], 'salt': result['salt'],
                'site_admin': result['site_admin']}

        with _cache_lock:
            _user_cache[user['username']] = user

        return user
    else:
        raise KeyError('User "{}" could not be found.'.format(username))


def get_user(username):
    with _cache_lock:
        user = _user_cache.get(username, None)

    if user is None:
        user = retrieve_user(username)

    return user


def log_in(sesh, username, password):
    try:
        user = get_user(username)
    except KeyError:
        raise ValueError('Username or password were invalid')

    salt = user.get('salt')
    hashed_pwd = hash_password(password, salt)

    if hashed_pwd == user.get('password_hash'):
        sesh['user'] = {'username': user.get('username'), 'site_admin': user.get('site_admin')}
    else:
        print('User "{}", failed login challenge.'.format(username))
        raise ValueError('Username or password were invalid.')
