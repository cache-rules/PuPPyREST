import bottle
from sqlalchemy.exc import IntegrityError
from puppy import post_service
from puppy.app import app


@app.route('/api/posts', ['GET', 'POST'])
def posts_route():
    session = bottle.request.environ.get('beaker.session')

    if bottle.request.method == 'POST':
        if session.get('user'):
            username = session['user']['username']
            data = bottle.request.json
            post_service.add_post(username, data.get('post'))
        else:
            bottle.abort(401)
    else:
        return {'posts': post_service.get_posts()}


@app.route('/api/posts/<post_id>', ['GET', 'DELETE'])  # No PUT here, we don't allow editing.
def post_route(post_id):
    if bottle.request.method == 'DELETE':
        return post_service.delete_post(post_id)
    else:
        return post_service.get_post(post_id)


@app.route('/api/posts/<post_id>/favorites', ['GET', 'POST'])
def post_favorites_route(post_id):
    session = bottle.request.environ.get('beaker.session')

    if bottle.request.method == 'POST':
        if session.get('user'):
            username = session['user']['username']
            print('adding fav for {}, from {}'.format(post_id, username))
            try:
                post_service.add_favorite(username, post_id)
                return {'success': True}
            except IntegrityError:
                # No duplicate favs!
                return {'success': True}
        else:
            bottle.abort(401)
    else:
        return post_service.get_favorites(post_id)
