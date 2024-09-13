from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS

# Initialize SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')
conn.commit()

@app.route('/register', methods=['POST'])
def register():
    user = request.json
    try:
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                       (user['username'], user['password'], user['email']))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    user = request.json
    cursor.execute('SELECT email FROM users WHERE username = ? AND password = ?', 
                   (user['username'], user['password']))
    result = cursor.fetchone()
    if result:
        return jsonify({"message": "Login successful", "email": result[0]})
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(port=5001, debug=True)
