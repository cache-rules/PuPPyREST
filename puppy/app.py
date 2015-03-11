import bottle
from beaker.middleware import SessionMiddleware
from waitress import serve
from puppy.database import init_database, init_engine

app = bottle.app()
bottle.debug(True)


def start_server(host, port, threads, db_config):
    init_engine(db_config)
    init_database()
    session_config = {
        'session.type': 'file',
        'session.cookie_expires': 60 * 60 * 24,  # Sessions expire after 24 hours.
        'session.data_dir': '.beaker/',
        'session.lock_dir': '.beaker/',
        'session.secret': "SHHH IT'S A SECRET!",  # Note: this should actually be a very long secret string (hash).
        'session.key': 'puget_sound_programming_python',
        'session.auto': True
    }
    app_with_sessions = SessionMiddleware(app, session_config)
    serve(app_with_sessions, host=host, port=port, threads=threads)