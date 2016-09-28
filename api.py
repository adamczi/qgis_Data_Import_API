# coding: utf-8
from flask import Flask, jsonify, abort, request
from config import *
from db import *
from models import *
import subprocess
import requests
import os

# app start
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/layers')
def layer():
    """ Get list of available data """
    layers = []
    x = db.execute_sql("""SELECT table_name FROM information_schema.tables WHERE TABLE_TYPE='BASE TABLE' and TABLE_SCHEMA = 'main';""")
    for sqlrow in x.fetchall():
        layers.append(list(sqlrow))

    ## Unnest list
    layers = sum(layers, [])

    ## Sort list
    layers.sort()

    return jsonify(layers)


@app.route('/<region>')
def temp(region):
    """ Download shp of selected table """
    api_key = request.headers.get('key')
    path = request.headers.get('path')

    ## Do sth with API key
    # api_key = api
    if api_key == '1234':

        path = os.path.normpath(path)

        print path

        command = ["pgsql2shp -f %s -h %s -u %s -P %s %s main.%s" % (path, host, user, pword, db_name, region)]
        print command

        try:
            ## Run pgsql2shp subprocess
            if os.name == 'posix':
                work = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                work = subprocess.Popen([command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = work.communicate()

            return 'success'
        except:
            return 'error'
    else:
        abort(401)

if __name__ == '__main__':
    app.secret_key = keySecret
    app.run(port=5000, debug=True)
