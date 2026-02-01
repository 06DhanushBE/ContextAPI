import secrets
import hashlib

def generate_api_key():
    raw_key = f"sk_{secrets.token_hex(24)}"
    return raw_key

def hash_api_key(api_key: str):
    return hashlib.sha256(api_key.encode()).hexdigest()
