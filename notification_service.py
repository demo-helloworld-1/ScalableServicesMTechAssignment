from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    notification = request.json
    print(f"Notification: {notification['message']}")
    return jsonify({"message": "Notification sent"}), 200

if __name__ == '__main__':
    app.run(port=5003, debug=True)
