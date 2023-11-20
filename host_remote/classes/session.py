import secrets
class Session():

    def __init__(self):
        self.counter = 0
    
    def generate_key(self){
        self.key = secrets.token_hex(16)
        self.counter += 1
        return self.key
    }

    def generate_one_time_password(self):
        data = f"{self.counter}:{self.key}".encode('utf-8')
        hashed_data = hashlib.sha256(data).hexdigest()
        self.otp = hashed_data[:6] 
        return self.otp  # Use the first 6 characters as the one-time password
        