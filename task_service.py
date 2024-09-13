import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
tasks = []

# Function to send notifications
def send_notification(subject, message, to):
    try:
        response = requests.post('http://localhost:5003/notify', json={"subject": subject, "message": message, "to": to})
        if response.status_code == 200:
            print("Notification sent successfully")
        else:
            print("Failed to send notification")
    except Exception as e:
        print("Error sending notification:", e)

# Function to check user authentication and get email
def authenticate_and_get_email(username, password):
    try:
        response = requests.post('http://localhost:5001/login', json={"username": username, "password": password})
        if response.status_code == 200:
            return response.json().get('email')
        return None
    except Exception as e:
        print("Error checking authentication:", e)
        return None

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    auth = request.authorization
    if not auth:
        return jsonify({"message": "Authentication required"}), 401
    email = authenticate_and_get_email(auth.username, auth.password)
    if not email:
        return jsonify({"message": "Authentication failed"}), 401
    task = request.json
    tasks.append(task)
    send_notification("Task Created", f"Task created: {task['title']}", email)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    auth = request.authorization
    if not auth:
        return jsonify({"message": "Authentication required"}), 401
    email = authenticate_and_get_email(auth.username, auth.password)
    if not email:
        return jsonify({"message": "Authentication failed"}), 401
    task = request.json
    tasks[task_id] = task
    send_notification("Task Updated", f"Task updated: {task['title']}", email)
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    auth = request.authorization
    if not auth:
        return jsonify({"message": "Authentication required"}), 401
    email = authenticate_and_get_email(auth.username, auth.password)
    if not email:
        return jsonify({"message": "Authentication failed"}), 401
    task = tasks.pop(task_id)
    send_notification("Task Deleted", f"Task deleted: {task['title']}", email)
    return '', 204

if __name__ == '__main__':
    app.run(port=5002, debug=True)
