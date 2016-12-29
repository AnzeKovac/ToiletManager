from .models import ToiletTime, ToiletStatus
from flask import jsonify, request, url_for, Response, abort
from . import app
from . import db
from datetime import datetime
from flask import Flask
from flask import render_template
from flask import jsonify, request, url_for, Response, abort
from flask.ext.sqlalchemy import SQLAlchemy

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
