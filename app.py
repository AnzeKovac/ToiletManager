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


class ToiletTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.String(80))
    datetime = db.Column(db.DateTime)

    def __init__(self, length):
        self.length = length
        self.datetime = datetime.utcnow()

    def __repr__(self):
        return '<Name %r>' % self.id

class ToiletStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    free = db.Column(db.String(80))
    datetime = db.Column(db.DateTime)

    def __init__(self,message):
        self.free = message
        self.datetime = datetime.utcnow()

    def __repr__(self):
        return '<Name %r>' % self.id


@app.route('/')
def home():
    status = ToiletStatus.query.order_by('-id').first()

    if(status):
        return status.free
    else:
        return "DB is empty"


@app.route('/freeUp/<int:length>', methods=['GET'])
def freeUp(length):
    toiletTime = ToiletTime(length)
    db.session.add(toiletTime)
    db.session.add(ToiletStatus("Toilet is free and ready to use."))
    db.session.commit()
    return "success"

@app.route('/busy', methods=['GET'])
def busy():
    toiletStatus = ToiletStatus("Someone is using the toilet.")
    db.session.add(toiletStatus)
    db.session.commit()
    return "success"



@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
