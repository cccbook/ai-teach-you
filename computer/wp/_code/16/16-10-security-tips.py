import secrets
from hashlib import scrypt

def hash_password_secure(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1)
    return f"{salt}${hashed.hex()}"

def verify_password_secure(password: str, stored_hash: str) -> bool:
    salt, hash_hex = stored_hash.split("$")
    expected = scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1).hex()
    return secrets.compare_digest(hash_hex, expected)

TIPS = [
    "Use HTTPS in production",
    "Store secrets in environment variables",
    "Implement rate limiting",
    "Validate all input on server side",
    "Use parameterized queries to prevent SQL injection",
    "Implement CSRF protection",
    "Use secure session management",
    "Keep dependencies updated",
    "Implement proper logging",
    "Use security headers (CSP, HSTS, etc.)"
]

if __name__ == "__main__":
    for tip in TIPS:
        print(f"- {tip}")
