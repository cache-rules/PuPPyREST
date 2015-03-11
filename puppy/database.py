from sqlalchemy import engine, create_engine, MetaData

db_metadata = MetaData()
db_engine = None


def init_engine(config):
    global db_engine

    eng_url = engine.url.URL('postgresql', **config)
    db_engine = create_engine(eng_url)


def clear_database():
    global db_metadata
    global db_engine

    db_metadata.drop_all(db_engine)


def __create_db_if_not_exists(url):
    """Checks to see if the user specified database exists, if not then we create it."""

    print('Checking if database exists')
    pg_url = engine.url.URL('postgresql', host=url.host, port=url.port, username=url.username,
                            password=url.password, database='postgres')
    pg_eng = engine.create_engine(pg_url)

    with pg_eng.connect() as conn:
        results = conn.execute("SELECT* FROM pg_database WHERE datname='{:s}'".format(url.database)).fetchall()

        if len(results) == 0:
            print('Creating new database with name "{:s}"'.format(url.database))
            conn.execute("commit")  # Postgres does not allow you to create databases in a transaction.
            conn.execute("CREATE DATABASE " + url.database)


def init_database():
    """
    Creates all the tables if needed. In the future it will also handle migrations.
    """
    global db_metadata
    global db_engine

    print('Initializing database')
    __create_db_if_not_exists(db_engine.url)
    db_metadata.create_all(db_engine)
