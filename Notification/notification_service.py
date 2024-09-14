import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

app = Flask(__name__)

# Email configuration
EMAIL_ADDRESS = 'demo.helloworld.1@gmail.com'
EMAIL_PASSWORD = 'ppbl uhzs tlaa bqgz'

def send_email(subject, body, to):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)

@app.route('/notify', methods=['POST'])
def notify():
    notification = request.json
    print(f"Notification: {notification['message']}")
    send_email(notification['subject'], notification['message'], notification['to'])
    return jsonify({"message": "Notification sent"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003,debug=True)
