from flask import Flask, Response, request
from cassandra.cluster import Cluster
import requests
import hashlib
import redis
import html
import sys

p = {'cassandra':
        {'ip': '192.168.99.100', 'port': 9042}
}

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
salt = "UNIQUE_SALT"
default_name="daisuke nishimura"


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


@app.route('/cassandra', methods=['GET', 'POST'])
def cassandra():

    if request.method == 'POST':
        form = request.form
    elif request.method == 'GET':
        form = request.args

    try:
        keyspace = html.escape(form.get('keyspace'), quote=True)

    except:
        keyspace = "firsttable"

    # param = json.loads(form.get('param'))

    str1, str2, str3, str4 = "", "", "", ""

    cluster = Cluster(contact_points=[p['cassandra']['ip']], port=p['cassandra']['port'])
    session = cluster.connect()

    try:
        query = "CREATE keyspace "+keyspace+" WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor': 2};"
        result = session.execute(query)

        str1 = keyspace + " CREATED"

    except:
        str1 = keyspace+"ALREAY THERE"

    #session.set_keyspace(keyspace)

    header = '<html><head><title>Cassandra Server</title></head><body>'
    body = '''
    {0}
    {1}
    {2}
    {3}
    '''.format(str1,str2,str3,str4)
    footer = '</body></html>'

    return header + body + footer


@app.route('/monster/<name>')
def get_identicon(name):

    name = html.escape(name, quote=True)
    image = cache.get(name)
    if image is None:

        #print("Cache miss")
        #print ("Cache miss", flush=True)

        r = requests.get('http://dnmonster:8080/monster/'+name+'?size=80')
        image = r.content
        cache.set(name, image)

    return Response(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


