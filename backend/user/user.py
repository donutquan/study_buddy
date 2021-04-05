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


# Get user by Username
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


# Get User by user_id
@app.route("/user/user_id/<string:user_id>")
def find_by_userId(user_id):
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

@app.route("/user/<string:username>", methods=['POST'])
def create_user(username):
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
    data = request.get_json()
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

    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201



# Does not work at the moment

# @app.route("/user/<string:username>", methods=['PUT'])
# def update_user(username):
#     try:
#         user = User.query.filter_by(username=username).first()

#         if not user:
#             return jsonify(
#             {
#                 "code": 404,
#                 "data": {
#                     "username": username
#                 },
#                 "message": "User not found."
#             }
#         ), 404

        
#         data = request.get_json()
#         if data['username']:
#             user.username = data['username']
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": user.json()
#                 }
#             ), 200
#         if data['telegram_id']:
#             user.username = data['telegram_id']
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": user.json()
#                 }
#             ), 200
#         if data['contact']:
#             user.contact = data['contact']
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": user.json()
#                 }
#             ), 200
#         if data['email']:
#             user.email = data['email'] 
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": user.json()
#                 }
#             ), 200
#         if data['photo']:
#             user.photo = data['photo'] 
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": user.json()
#                 }
#             ), 200
        
    
#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "username": username
#                 },
#                 "message": "An error occurred while updating the user. " + str(e)
#             }
#         ), 500  


@app.route("/user/<string:username>", methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "username": username
                },
                "message": "User " + username + " has been successfully removed"
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "username": username
            },
            "message": "User not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)