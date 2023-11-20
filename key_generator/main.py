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
    # Write the generated key to a file
    with open('generated_otp.txt', 'a') as file:
        file.write(f"{counter}: {generated_key}: {one_time_password}\n")

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

    expected_otp = session.generate_one_time_password()[:6]

    if received_otp == expected_otp:
        # Authentication successful
        session.reset()
        return jsonify({'success': True}), 200
    else:
        # Authentication failed
        return jsonify({'success': False}), 401
    

@app.route('/verify_credentials', methods=['POST'])
def authenticate():
    data = request.get_json()
    received_otp = data.get('pass')

    expected_otp = session.generate_one_time_password()[:6]

    if received_otp == expected_otp:
        # Authentication successful
        return jsonify({'success': True}), 200
    else:
        # Authentication failed
        return jsonify({'success': False}), 401


if __name__ == '__main__':
    app.run(port=5000)