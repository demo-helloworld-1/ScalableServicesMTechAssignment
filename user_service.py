from flask import Flask, request, jsonify

app = Flask(__name__)
users = {}

@app.route('/register', methods=['POST'])
def register():
    user = request.json
    users[user['username']] = {
        'password': user['password'],
        'email': user['email']
    }
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    user = request.json
    stored_user = users.get(user['username'])
    if stored_user and stored_user['password'] == user['password']:
        return jsonify({"message": "Login successful", "email": stored_user['email']})
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(port=5001, debug=True)
