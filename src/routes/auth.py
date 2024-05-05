import bcrypt
from src.app import app
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
import json

users = {}

# Note: now with the JWT, endpoints can use @jwt_required() to enforce a token

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = json.loads(request.data.decode('utf-8'))

    # data = request.json
    username = data.get('username')
    password = data.get('password')
    print(1)
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    print(2)
    token = create_access_token(identity=username, expires_delta=False)
    if username not in users:
        print(3)
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Store the user in the dictionary (in the future we will use database)
        users[username] = {'username': username, 'password': hashed_password, 'google': False}  
        print(4)
        response = jsonify({'message': 'Success', 'token': token})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        print(5)
        if bcrypt.checkpw(password.encode('utf-8'), users[username][password]):
            print(6)
            return jsonify({'message': 'Success', 'token': token}), 200
    print(7)
    return jsonify({'message': 'Unable to authenticate', 'token': None}), 403

@app.route('/google_authenticated', methods=['POST'])
def authenticated_user_data():
    data = request.json
    username = data.get('username')
    token = create_access_token(identity=username, expires_delta=False)

    if username not in users:
        users[username] = {'username': username, 'password': "google-protected", 'google': True}
        return jsonify({'message': 'Success', 'token': token}), 201
    
    return jsonify({'message': 'Success', 'token': token}), 200

@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    data = request.json
    username = data.get('username')

    del users[username]
    return {"message": "Logged out successfully"}

