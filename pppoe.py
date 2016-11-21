import re
from subprocess import check_output, CalledProcessError

from flask import Flask
from functools import wraps
from flask import request, Response

cmd_start = 'pppoe-start'
cmd_stop = 'pppoe-stop'
cmd_status = 'pppoe-status'
need_auth = True
auth_user = 'admin'
auth_pass = '123456'


def check_auth(username, password):
    if need_auth:
        return username == auth_user and password == auth_pass
    else:
        return True


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


class Pppoe():
    def get_ip(self, text):
        try:
            pattern = re.compile('inet (\d+\.\d+\.\d+\.\d+)', re.S)
            result = re.search(pattern, text)
            if result:
                return result.group(1)
            else:
                return None
        except TypeError:
            return None

    def repppoe(self):
        try:
            result = ''
            result += check_output(cmd_stop)
            result += check_output(cmd_start)
            result += check_output(cmd_status)
            return result
        except (CalledProcessError, FileNotFoundError) as e:
            return e


app = Flask(__name__)
pppoe = Pppoe()


@app.route('/repppoe')
@requires_auth
def repppoe():
    result = pppoe.repppoe()
    ip = pppoe.get_ip(result)
    return ip


if __name__ == '__main__':
    app.run(host='0.0.0.0')
