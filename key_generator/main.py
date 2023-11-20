from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from classes.session import Session
from classes.user import User

app = Flask(__name__)
auth = HTTPBasicAuth()

session = Session()
user = User("admin", "admin")

@auth.verify_password
def verify_password(username, password):
    return username == user.username and password == user.password


@app.route('/generate_credentials', methods=['POST'])
@auth.login_required
def generate_credentials():
    # Generate a key using the Session class
    generated_key = session.generate_key()
    one_time_password = session.generate_one_time_password()
    counter = session.counter

    return jsonify({'success': True}), 200

@app.route('/get_otp', methods=['POST'])
@auth.login_required
def generate_one_time_password():
    # Generate a one-time password using the Session class
    one_time_password = session.generate_one_time_password()

    return jsonify({'one_time_password': one_time_password}), 200

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    received_otp = data.get('pass')

    expected_otp = session.generate_one_time_password()

    if received_otp == expected_otp:
        # Authentication successful
        session.reset()
        return jsonify({'success': True}), 200
    else:
        # Authentication failed
        return jsonify({'success': False}), 401
    

@app.route('/verify_credentials', methods=['POST'])
def verify_credentials():
    data = request.get_json()
    received_otp = data.get('pass')

    expected_otp = session.generate_one_time_password()

    if received_otp == expected_otp:
        # Authentication successful
        return jsonify({'success': True}), 200
    else:
        # Authentication failed
        return jsonify({'success': False}), 401


@app.route('/delete_session', methods=['POST'])
def delete_session():
    session.reset()
    return jsonify({'success': True}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)