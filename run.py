import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY']='bashman'


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db = SQLAlchemy(app)
Migrate(app,db)

class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.Text)
    password=db.Column(db.Text)

    def __init__(self,name):
        self.name=name

    # def __repr__(self):
    #     if




@app.route('/')
def index():
    return "Hello Threre ArtAdherence"

@app.route('/users', methods=['POST'])
def users():
    data = request.get_json()

    id=data.get('id')
    username=data.get('username')
    password=data.get('password')





if __name__ == '__main__':
    app.run(debug=True)