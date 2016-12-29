
import os
from datetime import datetime
from flask import Flask
from flask import render_template
from flask import jsonify, request, url_for, Response, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wgvuxwygmotxes:959d85bab96341ed347990418440a2036e9a084ab84d36fe4fd2b20f648d17f3@ec2-79-125-13-42.eu-west-1.compute.amazonaws.com:5432/dbl9hh8u7n790v'
#os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# import routes after we initialize "app" and "db"
from . import routes
