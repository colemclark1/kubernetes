from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin 
import os
from flask_migrate import Migrate
import sys

print('This is error output', file=sys.stderr)
print('This is standard output', file=sys.stdout)


# python -m pipenv shell
# python app.py

# flask db migrate -m "Initial migration."   -> This is to make a migration. Must be in pipenv and use 'python -m' prefix

#Init app
app = Flask(__name__)
CORS(app, support_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, firstName, lastName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", 'firstName', 'lastName', 'email')
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user/<id>', methods=["POST"])
@cross_origin(supports_credentials=True)
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/user', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/user', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_user():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']

    new_user = User(firstName, lastName, email)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/user', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update_user():
    x = User.query.get(request.json['id'])
    x.firstName = request.json['firstName']
    x.lastName = request.json['lastName']
    x.email = request.json['email']

    db.session.commit()
    return user_schema.jsonify(x)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
