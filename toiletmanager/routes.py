from .models import ToiletTime, ToiletStatus, QueueCandidate
from flask import jsonify, request, url_for, Response, abort
from . import app
from . import db
from datetime import datetime
from flask import Flask
from flask import render_template
from flask import jsonify, request, url_for, Response, abort
from flask.ext.sqlalchemy import SQLAlchemy
from urllib.parse import urlencode
from urllib.request import Request, urlopen

@app.route('/')
def index():
        return "Your token is shitty shitty. No API for you. Pitty pitty."

@app.route('/status', methods=['GET'])
def home():
    params = request.args
    returnUrl = params['response_url'] if 'response_url' in params else None
    request = params
    status = ToiletStatus.query.order_by('-id').first()

    if(status):
        if status.free == 'Someone is using the toilet.':
            db.session.add(QueueCandidate(returnUrl))
            db.session.commit()
        return status.free
    else:
        return "DB is empty"


@app.route('/freeUp/<int:length>', methods=['GET'])
def freeUp(length):
    toiletTime = ToiletTime(length)
    db.session.add(toiletTime)
    db.session.add(ToiletStatus("Toilet is free and ready to use."))
    db.session.commit()

    #send notification to all in queue
    candidates = QueueCandidate.query.all()
    for candidate in candidates:
        url = candidate.returnUrl # Set destination URL here
        post_fields = {'response_type': 'ephemeral','text':'Toilet is free. Run run run!!!'}     # Set POST fields here

        request = Request(url, urlencode(post_fields).encode())
        json = urlopen(request).read().decode()
        print(json)
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

@app.route('/schema')
def schema():
    db.create_all()
    db.session.commit()
    return 'success'



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
