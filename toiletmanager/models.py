from . import db
from datetime import datetime

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

class QueueCandidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    returnUrl = db.Column(db.DateTime)
    datetime = db.Column(db.DateTime)

    def __init__(self,url):
        self.free = url
        self.datetime = datetime.utcnow()

    def __repr__(self):
        return '<returnUrl %r>' % self.returnUrl
