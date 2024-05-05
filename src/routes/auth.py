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

    username = data.get('username')
    password = data.get('password')
    print(username)
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    token = create_access_token(identity=username, expires_delta=False)
    if username not in users:
        print('New default account created')

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Store the user in the dictionary (in the future we will use database)
        users[username] = {'username': username, 'password': hashed_password, 'google': False}  

        return jsonify({'message': 'Success', 'token': token}), 201
    else:
        if bcrypt.checkpw(password.encode('utf-8'), users[username]["password"].encode('utf-8')):
            print('Signed in with existing default account')

            return jsonify({'message': 'Success', 'token': token}), 200
        
    return jsonify({'message': 'Unable to authenticate', 'token': None}), 403

@app.route('/google_authenticated', methods=['POST'])
def authenticated_user_data():
    data = json.loads(request.data.decode('utf-8'))

    username = data.get('username')
    token = create_access_token(identity=username, expires_delta=False)
    print(username)
    if username not in users:
        print('New google account created')

        users[username] = {'username': username, 'password': "google-protected", 'google': True}
        return jsonify({'message': 'Success', 'token': token}), 201

    print('Signed in with existing google account')
    return jsonify({'message': 'Success', 'token': token}), 200

@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    data = request.json
    username = data.get('username')

    # del users[username]
    return {"message": "Logged out successfully"}

