from flask import Blueprint, request, jsonify
# this is for making random passowrd library
from werkzeug.security import generate_password_hash, check_password_hash
# importing database
from models import db
from models.user_model import User

# blueprint for authentication
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    # This will get the data that we get from js and add it to variable
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    username = data.get('username')
    password = data.get('password')

    # checks if user exist
    existing_user = User.query.filter_by(username=username).first()
    # if so then says user already exist
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    # If not then makes the passowrd diffrent
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    # The the object to new_user
    new_user = User(
        firstname=firstname,
        lastname=lastname,
        username=username,
        password=hashed_password,
    )
    # adds new user and commits 
    db.session.add(new_user)
    db.session.commit()
    # message to show 
    return jsonify({"message": f"User {firstname} {lastname} registered successfully"}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Verify user credentials
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    # Include user_id in the response
    return jsonify({
        "message": f"Welcome back, {username}!",
        "user_id": user.id,
        "firstname": user.firstname
    }), 200


@auth_blueprint.route('/getFirstname', methods=['POST'])
def get_firstname():
    data = request.get_json()
    username = data.get('username')

    # Query the User table for the username
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Return the first name
    return jsonify({"firstname": user.firstname}), 200

@auth_blueprint.route('/buyers_power', methods=['GET'])
def get_buyers_power():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"buyers_power": user.buyers_power}), 200
