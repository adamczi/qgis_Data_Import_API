# coding: utf-8
from flask import Flask, jsonify, abort, Response
from config import *
from db import *
from models import *
# from peewee import fn
import subprocess

#app start
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

@app.route('/<api>/<region>/<path:path>')
def temp(api, path, region):
    """ Download shp of selected table """
    
    ## Do sth with API key
    api_key = api
    
    ## Strip the 'path' word
    path = path[4:]
    
    command = ["pgsql2shp -f %s -h %s -u %s -P %s db_name %s" % (path, host, user, password, region)] 

    try:
        ## Run pgsql2shp subprocess 
        work = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = work.communicate()

        return 'success'
    except:
        return 'error'

if __name__ == '__main__':
    app.secret_key = keySecret
    app.run(port=5000, debug=True)
