import os

from datetime import datetime
from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class ToiletTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.String(80))
    datetime = db.Column(db.DateTime)

    def __init__(self, length):
        self.length = length
        self.datetime = datetime.utcnow()

    def __repr__(self):
        return '<Name %r>' % self.name


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    params = request.args
    length = params['lenght'] if 'length' in parameters else 0



@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
