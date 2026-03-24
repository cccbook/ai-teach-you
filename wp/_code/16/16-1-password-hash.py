from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

if __name__ == "__main__":
    hashed = hash_password("mysecretpassword")
    print(f"Hashed: {hashed}")
    print(f"Verify: {verify_password('mysecretpassword', hashed)}")
    print(f"Wrong: {verify_password('wrongpassword', hashed)}")
