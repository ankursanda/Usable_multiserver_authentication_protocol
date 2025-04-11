from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


class Crypto_keys():
    def __init__(self):
        self.private_key = ''
        self.public_key = ''
    def generate_keys(self):
        # Generate ECC Private Key
        private_key = ec.generate_private_key(ec.SECP256R1())  # NIST P-256 curve

        # Generate Public Key
        public_key = private_key.public_key()

        # Serialize Keys for Sharing/Storage
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        self.private_key = private_bytes.decode()
        self.public_key = public_bytes.decode()

    def get_keys(self):
        if not self.private_key or not self.public_key:
            return "Not generated keys yet"
        else:
            return (self.private_key,self.public_key)
# print("Private Key:", private_bytes.decode())
# print("Public Key:", public_bytes.decode())
