from .models import ToiletTime, ToiletStatus, QueueCandidate, Menu
from flask import jsonify, request, url_for, Response, abort
from . import app
from . import db
from datetime import datetime
from flask import Flask
from flask import render_template
from flask import jsonify, request, url_for, Response, abort
from flask.ext.sqlalchemy import SQLAlchemy
from urllib.parse import urlencode
from slacker import Slacker
import urllib.request
import urllib
import json
import os
import time


@app.route('/')
def index():
        return "Service is in maintenance."

@app.route('/status', methods=['GET'])
def home():
    params = request.args
    returnUrl = params['response_url'] if 'response_url' in params else None
    reservation = params['text'] if 'text' in params else None
    status = ToiletStatus.query.order_by('-id').first()

    if(status):
        if status.free == "Someone is using the toilet.I will remind you when it's free again." or "Toiled is reservated. You are in the queue":
            if(returnUrl):
                return_url = urllib.request.unquote(returnUrl)
                db.session.add(QueueCandidate(return_url))
                db.session.commit()
                return status.free
        elif reservation and reservation == "reserve":
            toiletStatus = ToiletStatus("Toiled is reservated. You are in the queue.")
            db.session.add(toiletStatus)
            db.session.commit()
            #Hold reservation for 30 seconds
            time.sleep(30);
            status = ToiletStatus.query.order_by('-id').first()
            if status.free == "Toilet is free and ready to use.":
                toiletTime = ToiletTime(30)
                db.session.add(toiletTime)
                db.session.add(ToiletStatus("Toilet is free and ready to use."))
                return 'Your reservation has ended.'
            return 'Reservation was used'
            
        else:
            return status.free
    else:
        return "DB is empty"


@app.route('/freeUp/<int:length>', methods=['GET'])
def freeUp(length):
    toiletTime = ToiletTime(length)
    db.session.add(toiletTime)
    db.session.add(ToiletStatus("Toilet is free and ready to use."))

    #send notification to first in queue
    candidate = QueueCandidate.query.first()

    url = candidate.return_url # Set destination URL here
    if(url):
        data = {'response_type': 'ephemeral','text':'Toilet is now free.'}
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(data)
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))
        urllib.request.urlopen(req, jsondataasbytes)
     #Remove candidate
    QueueCandidate.query.delete(candidates)
    db.session.commit()
    return "success"

@app.route('/busy', methods=['GET'])
def busy():
    toiletStatus = ToiletStatus("Someone is using the toilet.I will remind you when it's free again.")
    db.session.add(toiletStatus)
    db.session.commit()
    return "success"

@app.route('/changeMenu', methods=['POST'])
def menuChange():
    currentMenu = Menu.query.delete()
    if request.headers['Content-Type'] == 'application/json':
        concat = ''
        for item in request.json:
            menuItem = Menu(item)
            db.session.add(menuItem)
    db.session.commit()
    startProcess()
    return concat

@app.route('/start', methods=['GET'])
def startProcess():
    todayMenu = Menu.query.all()
    message = '*Danes vam ponujamo:*\n'
    for menuItem in todayMenu:
        message+='• '+menuItem.item+'\n'
    message += '\nDober tek!'
    token = os.environ['TOKEN']
    slack = Slacker(token)
    slack.chat.post_message('#kosilo', message,icon_emoji=':pizza:',username='Element')
    return 'success'



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
