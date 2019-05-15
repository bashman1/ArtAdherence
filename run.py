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

    def __init__(self, username, password):
        # self.id=id
        self.username=username
        self.password=password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password','id')



user_schema = UserSchema()
user_schema = UserSchema(many=True)


# The root page route
@app.route('/')
def index():
    return jsonify({"message":"Hello Threre ArtAdherence"})


# Register user route

@app.route('/users', methods=['POST'])
def users():
    data = request.get_json()

    id=data.get('id')
    username=data.get('username')
    password=data.get('password')

    new_user = User(username, password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({username: "registered"})  #


# Get all users route

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = user_schema.dump(all_users)
    return jsonify(result.data)

# Get specific user route

@app.route('/users/<id>', methods=['GET'])
def get_specific_user(id):
    user = User.query.get(id)
    return user_schema.jsonify({user})

# Updating a specific user route

@app.route('/users/<id>', methods=['PUT'])
def  update_specific_user(id):
    user = User.query.get(id)
    username=request.json['username']
    password = request.json['password']

    user.username=username
    user.password=password

    db.session.commit()
    return user_schema.jsonify({user})


# Deleting a specific user route

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    if user>0:
        return user_schema.jsonify({user})



if __name__ == '__main__':
    app.run(debug=True)
