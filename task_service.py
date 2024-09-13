import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
tasks = []

# Function to send notifications
def send_notification(message):
    try:
        response = requests.post('http://localhost:5003/notify', json={"message": message})
        if response.status_code == 200:
            print("Notification sent successfully")
        else:
            print("Failed to send notification")
    except Exception as e:
        print("Error sending notification:", e)

# Function to check user authentication
def is_authenticated(username, password):
    try:
        response = requests.post('http://localhost:5001/login', json={"username": username, "password": password})
        return response.status_code == 200
    except Exception as e:
        print("Error checking authentication:", e)
        return False

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    auth = request.authorization
    if not auth or not is_authenticated(auth.username, auth.password):
        return jsonify({"message": "Authentication required"}), 401
    task = request.json
    tasks.append(task)
    send_notification(f"Task created: {task['title']}")
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    auth = request.authorization
    if not auth or not is_authenticated(auth.username, auth.password):
        return jsonify({"message": "Authentication required"}), 401
    task = request.json
    tasks[task_id] = task
    send_notification(f"Task updated: {task['title']}")
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    auth = request.authorization
    if not auth or not is_authenticated(auth.username, auth.password):
        return jsonify({"message": "Authentication required"}), 401
    task = tasks.pop(task_id)
    send_notification(f"Task deleted: {task['title']}")
    return '', 204

if __name__ == '__main__':
    app.run(port=5002, debug=True)
