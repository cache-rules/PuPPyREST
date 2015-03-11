import bottle
from puppy import user_service
from puppy.helpers import requires_session
from puppy.template import template
from puppy.app import app


@app.route('/assets/<filename:path>', ['GET'])
def send_static(filename):
    """Route the core static assests"""
    if filename.endswith(".woff"):
        return bottle.static_file(filename, root='web', mimetype='application/font-woff')
    else:
        return bottle.static_file(filename, root='web')

@app.route('/', ['GET'])
@requires_session
def index(sesh):
    if sesh.get('user', False):
        bottle.redirect('/dashboard')

    return template('index.html')


@app.route('/add_user', ['GET', 'POST'])
def add_user_page():
    if bottle.request.method == 'POST':
        form = bottle.request.params
        user_service.create_user(form.username, form.password, True)
        bottle.redirect('/')
    else:
        return template('add_user.html')


@app.route('/log_out', ['GET'])
@requires_session
def log_out_page(sesh):
    sesh.delete()
    bottle.redirect('/')


@app.route('/dashboard', ['GET'])
@requires_session
def posts_page(sesh):
    user = sesh.get('user', None)
    if user:
        return template('dashboard.html', user=user)
    else:
        bottle.redirect('/')