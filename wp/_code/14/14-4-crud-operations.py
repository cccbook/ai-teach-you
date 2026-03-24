from sqlalchemy.orm import Session
from 14-1-sqlalchemy-basic import User, engine

SessionLocal = sessionmaker(bind=engine)

def create_user(db: Session, name: str, email: str):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, **kwargs):
    user = db.query(User).filter(User.id == user_id).first()
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.commit()
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    return {"message": "Deleted"}
