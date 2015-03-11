from puppy.app import start_server


if __name__ == "__main__":
    db_config = {
        'username': 'puppy',
        'password': 'puppy',
        'host': 'localhost',
        'port': 5432,
        'database': 'puppy'
    }

    start_server('0.0.0.0', 8000, 4, db_config)