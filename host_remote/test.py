from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import hashlib
import secrets
def generate_one_time_password(secret_key, counter):
    data = f"{counter}:{secret_key}".encode('utf-8')
    hashed_data = hashlib.sha256(data).hexdigest()
    return hashed_data[:6]  # Use the first 6 characters as the one-time password


secret_key_docker = "your_secret_key_docker"
counter_docker = 1 

print(generate_one_time_password(secret_key_docker, counter_docker))