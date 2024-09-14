import sqlite3
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Initialize SQLite database
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()

# Create or modify the tasks table to include 'status' column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        username TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Yet to Start'  -- New column for task status
    )
''')
conn.commit()

# Function to send notifications
def send_notification(subject, message, to):
    try:
        response = requests.post('http://notification-service:5003/notify', json={"subject": subject, "message": message, "to": to})
        if response.status_code == 200:
            print("Notification sent successfully")
        else:
            print("Failed to send notification")
    except Exception as e:
        print("Error sending notification:", e)

# Function to validate user via the user-service
def is_valid_user(username, password):
    try:
        response = requests.post('http://user-service:5001/login', json={"username": username, "password": password})
        if response.status_code == 200:
            return True  # Valid user
        else:
            return False  # Invalid user
    except Exception as e:
        print("Error validating user:", e)
        return False

@app.route('/tasks', methods=['GET'])
def get_tasks():
    print("Received GET request for tasks")
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    print("Tasks fetched:", tasks)
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    print("Received POST request to add task")
    task = request.json
    
    # Validate the user before adding the task
    username = task.get('username')
    password = task.get('password')
    status = task.get('status', 'Yet to Start')  # Default status if not provided
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    if not is_valid_user(username, password):
        return jsonify({"message": "Invalid user credentials"}), 401
    
    # User is valid, add the task
    cursor.execute('INSERT INTO tasks (title, description, username, status) VALUES (?, ?, ?, ?)', 
                   (task['title'], task['description'], username, status))
    conn.commit()
    send_notification("Task Created", f"Task created: {task['title']}", "dhanudhanudhanub@gmail.com")
    print("Task added:", task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    print(f"Received PUT request to update task {task_id}")
    task = request.json
    
    # Validate the user before updating the task
    username = task.get('username')
    password = task.get('password')
    status = task.get('status', 'Yet to Start')  # Default status if not provided
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    if not is_valid_user(username, password):
        return jsonify({"message": "Invalid user credentials"}), 401
    
    # User is valid, update the task
    cursor.execute('UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?', 
                   (task['title'], task['description'], status, task_id))
    conn.commit()
    send_notification("Task Updated", f"Task updated: {task['title']}", "dhanudhanudhanub@gmail.com")
    print("Task updated:", task)
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    print(f"Received DELETE request to delete task {task_id}")
    task = request.json
    
    # Validate the user before deleting the task
    username = task.get('username')
    password = task.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    if not is_valid_user(username, password):
        return jsonify({"message": "Invalid user credentials"}), 401
    
    # User is valid, delete the task
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    send_notification("Task Deleted", f"Task deleted: {task_id}", "dhanudhanudhanub@gmail.com")
    print(f"Task {task_id} deleted")
    return '', 204

# Add the simple endpoint here
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
