from encriptUtils import Crypto_keys
from dotenv import load_dotenv
import os
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
import requests
import base64

load_dotenv()

secret_value_y = os.getenv('SECRET_VALUE_Y')
user_id = os.getenv('USER_ID')
password = os.getenv('PASSWORD')


combined = secret_value_y.encode() + user_id.encode() + password.encode()
a_i = hashlib.sha256(combined).digest()

user_crypto_instance = Crypto_keys()
user_crypto_instance.generate_keys()

priv,  pub = user_crypto_instance.get_keys()

private_key = serialization.load_pem_private_key(priv.encode(), password=None)
public_key = serialization.load_pem_public_key(pub.encode())

q_int = private_key.private_numbers().private_value  # integer
q_bytes = q_int.to_bytes(32, 'big')  # Convert to 32-byte big-endian

# XOR q with Ai to get Ei
Ei = bytes(a ^ b for a, b in zip(q_bytes, a_i))

# Base64 encode the original Ai to send to server
a_i_encoded = base64.b64encode(a_i).decode('utf-8')

# headers = {
#     "X-API-Key": "123",
#     "Content-Type": "application/json"
# }

data = {'user_id': user_id, 'A_i': a_i_encoded}
response = requests.post('http://localhost:5000/api/v1/register/user', json=data)
print(response.status_code)
print(response.json())

#printing for testing
print('The variable a_i (raw):', a_i)
print('The variable a_i (base64):', a_i_encoded)
print("The private key is:", private_key)
print("The public key is:", public_key)
print("The final value of Ei is:", Ei)