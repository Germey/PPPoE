import re
from subprocess import check_output, CalledProcessError

from flask import Flask

cmd_start = 'pppoe-start'
cmd_stop = 'pppoe-stop'
cmd_status = 'pppoe-status'


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
def repppoe():
    result = pppoe.repppoe()
    print(result)
    ip = pppoe.get_ip(result)
    return ip


if __name__ == '__main__':
    app.run()
