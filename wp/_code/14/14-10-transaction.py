from sqlalchemy.orm import Session
from 14-1-sqlalchemy-basic import User, engine
from sqlalchemy.exc import SQLAlchemyError

SessionLocal = sessionmaker(bind=engine)

def transaction_demo():
    db = SessionLocal()
    try:
        db.begin()
        
        user1 = User(name="User 1", email="user1@example.com")
        user2 = User(name="User 2", email="user2@example.com")
        
        db.add_all([user1, user2])
        db.flush()
        
        db.commit()
        print("Transaction committed!")
        
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Transaction rolled back: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    transaction_demo()
