import bcrypt
from src.app import app, db
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
    print('Sign in attempt: ', username)

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    user_doc = db.collection('users').document(username).get()
    if user_doc.exists:
        # Existing user login
        user_data = user_doc.to_dict()
        if not user_data:
            return jsonify({'error': 'Invalid user data'}), 500

        if bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
            token = create_access_token(identity=username, expires_delta=False)
            return jsonify({'message': 'Success', 'token': token}), 200
        
        return jsonify({'message': 'Incorrect password', 'token': None}), 403
    else:
        # New user registration
        print('New default account created: ', username)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.collection('users').document(username).set({
            'username': username,
            'password': hashed_password,
        })

        token = create_access_token(identity=username, expires_delta=False)
        return jsonify({'message': 'Success', 'token': token}), 201


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

