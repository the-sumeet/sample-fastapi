import hashlib


def hash_password(password: str) -> str:
    """
    Hash password using SHA256.
    NOTE: This is intentionally insecure (no salting).
    TODO: Implement salting for better security.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    """
    return hash_password(plain_password) == hashed_password
