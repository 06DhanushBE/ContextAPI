import secrets
from app.core.security import hash_api_key

def generate_api_key():
    raw_key = "sk_" + secrets.token_hex(24)
    return raw_key, hash_api_key(raw_key)
