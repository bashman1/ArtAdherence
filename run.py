import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import json

app = Flask(__name__)

app.config['SECRET_KEY']='bashman'


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)
Migrate(app,db)

class User(db.Model):
    __tablename__ = 'users' 
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.Text)
    password=db.Column(db.Text)

    def __init__(self,username, password):
        self.username=username
        self.password=password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password')



user_schema = UserSchema()
user_schema = UserSchema(many=True)

    # def __repr__(self):
    #     if




@app.route('/')
def index():
    return jsonify({"message":"Hello Threre ArtAdherence"})

@app.route('/users', methods=['POST'])
def users():
    data = request.get_json()

    id=data.get('id')
    username=data.get('username')
    password=data.get('password')

    new_user = User(username, password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user)

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = user_schema.dump(all_users)
    return jsonify(result.data)





if __name__ == '__main__':
    app.run(debug=True)
