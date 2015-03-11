from functools import wraps
import bottle


def requires_session(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        sesh = bottle.request.environ.get('beaker.session')
        kwargs['sesh'] = sesh
        return fun(*args, **kwargs)

    return wrapper


def requires_login(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        sesh = bottle.request.environ.get('beaker.session')

        if 'user' in sesh and 'id' in sesh['user']:
            return fun(*args, **kwargs)
        else:
            bottle.abort(401, 'User must be logged in.')

    return wrapper


def requires_site_admin(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        sesh = bottle.request.environ.get('beaker.session')

        if 'user' in sesh and sesh['user']['site_admin'] is True:
            return fun(*args, **kwargs)
        else:
            bottle.abort(401, 'Site admin privileges required.')

    return wrapper