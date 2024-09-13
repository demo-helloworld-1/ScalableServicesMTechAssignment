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

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json
    tasks.append(task)
    send_notification(f"Task created: {task['title']}")
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = request.json
    tasks[task_id] = task
    send_notification(f"Task updated: {task['title']}")
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = tasks.pop(task_id)
    send_notification(f"Task deleted: {task['title']}")
    return '', 204

if __name__ == '__main__':
    app.run(port=5002, debug=True)
