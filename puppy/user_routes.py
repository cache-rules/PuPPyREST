from bottle import request, response
from puppy.app import app
from puppy.helpers import requires_session
import puppy.user_service as user_service


@app.route('/api/login', ['POST'])
@requires_session
def log_in(sesh=None):
    if request.json is None:
        response.status = 400
        return {'success': False, 'error': 'Request must include a JSON payload'}

    try:
        username = request.json['username']
    except KeyError:
        response.status = 400
        return {'success': False, 'error': 'Request payload must include email.'}

    try:
        password = request.json['password']
    except KeyError:
        response.status = 400
        return {'success': False, 'error': 'Request payload must include password.'}

    try:
        user_service.log_in(sesh, username, password)
    except ValueError as e:
        response.status = 400
        return {'success': False, 'error': str(e)}

    return {'success': True}


@app.route('/api/logout', ['POST'])
@requires_session
def logout(sesh=None):
    sesh.delete()
    return {'success': True}

