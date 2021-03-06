from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    telegram_id = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    photo = db.Column(db.String(45), nullable=False)
    account_num = db.Column(db.Integer, nullable=False)
    account_type = db.Column(db.String(20), nullable=False)
    bank_name = db.Column(db.String(20), nullable=False)

    def __init__(self, user_id, username, telegram_id, contact, email, photo, account_num, account_type, bank_name):
        self.user_id = user_id
        self.username = username
        self.telegram_id = telegram_id
        self.contact = contact
        self.email = email
        self.photo = photo
        self.account_num = account_num
        self.account_type = account_type
        self.bank_name = bank_name

    def json(self):
        return {"user_id": self.user_id, 
                "username": self.username, 
                "telegram_id": self.telegram_id, 
                "contact": self.contact, 
                "email": self.email, 
                "photo": self.photo, 
                "account_num": self.account_num, 
                "account_type": self.account_type, 
                "bank_name": self.bank_name}

# Get All Users
@app.route("/user")
def get_all():
    userlist = User.query.all()
    if len(userlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in userlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404


# Get a Single User by Username
@app.route("/user/username/<string:username>")
def find_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404


# Get a Single User by User Id
@app.route("/user/user_id/<string:user_id>")
def find_by_user_id(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404


# Add a new User
@app.route("/user/addUser", methods=['POST'])
def create_user():
    data = request.get_json()
    if data['username']:
        username = data['username']
        if (User.query.filter_by(username=username).first()):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "username": username
                    },
                    "message": "User already exists."
                }
            ), 400
        user = User(None, **data)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "username": username
                    },
                    "message": "An error occurred creating the user."
                }
            ), 500
    else:
        return jsonify(
            {
                "code": 400,
                "message": "An error occurred creating the user, username was not given."
            }
        ), 400

    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201


# Delete a User
@app.route("/user/deleteUser", methods=['DELETE'])
def delete_user():
    data = request.get_json()
    if data['user_id']:
        user_id = data['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "user_id": user_id
                    },
                    "message": "User " + str(user_id) + " has been successfully removed"
                }
            )
        return jsonify(
            {
                "code": 404,
                "data": {
                    "user_id": user_id
                },
                "message": "User not found."
            }
        ), 404
    else:
        return jsonify(
            {
                "code": 400,
                "message": "An error occurred deleting the user, user_id was not given."
            }
        ), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)