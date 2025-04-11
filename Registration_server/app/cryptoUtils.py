from cryptography.hazmat.primitives import hashes



class CryptoUtils:
    @staticmethod
    def hash_value(value: bytes) -> bytes:
        """Create SHA-256 hash of input value"""
        digest = hashes.Hash(hashes.SHA256())
        digest.update(value)
        return digest.finalize()
    
    @staticmethod
    def xor_bytes(a: bytes, b: bytes) -> bytes:
        """XOR two byte strings"""
        return bytes(x ^ y for x, y in zip(a, b))
