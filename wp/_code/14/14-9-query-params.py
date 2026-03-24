from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from 14-1-sqlalchemy-basic import User, engine

SessionLocal = sessionmaker(bind=engine)

def advanced_queries():
    db = SessionLocal()
    
    users = db.query(User).filter(
        or_(User.name.like("A%"), User.email.endswith("@example.com"))
    ).all()
    
    users_sorted = db.query(User).order_by(desc(User.name)).all()
    
    users_paginated = db.query(User).offset(0).limit(10).all()
    
    db.close()
    return users, users_sorted, users_paginated

def search_users(db: Session, keyword: str, skip: int = 0, limit: int = 10):
    return db.query(User).filter(
        or_(
            User.name.ilike(f"%{keyword}%"),
            User.email.ilike(f"%{keyword}%")
        )
    ).offset(skip).limit(limit).all()
