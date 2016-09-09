from flask import Flask, Response, request, send_from_directory
from cassandra.cluster import Cluster
import requests
import hashlib
import redis
import html
import sys
import os

p = {'cassandra':
        {'ip': '192.168.99.100', 'port': 9042}
}

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
salt = "UNIQUE_SALT"
default_name="daisuke nishimura"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', 'POST'])
def mainpage():

    name = default_name
    if request.method == 'POST':
        #name = request.form['name']
        name = html.escape(request.form['name'], quote=True)

    salted_name = salt + name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

    header = '<html><head><title>Cassandra Server</title></head><body>'
    body = '''
        <form method="POST">
        Hello <input type="text" name="name" value="{0}">
        <input type="submit" value="submit">
        </form>
        <p>You look like a :
        <img src="/monster/{1}"/>
    '''.format(name, name_hash)
    footer ='</body></html>'

    return header+body+footer





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


