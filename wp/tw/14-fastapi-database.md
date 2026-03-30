# 第 14 章：FastAPI 資料庫

## 概述

本章介紹如何在 FastAPI 中整合資料庫，使用 SQLAlchemy ORM 進行資料庫操作。

## 14.1 SQLAlchemy 基礎

SQLAlchemy 是 Python 最流行的 ORM 工具。

[程式檔案：14-1-sqlalchemy-basic.py](../_code/14/14-1-sqlalchemy-basic.py)

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)

engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 14.2 ORM 模型定義

定義資料庫表結構。

[程式檔案：14-2-orm-model.py](../_code/14/14-2-orm-model.py)

```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from 14-1-sqlalchemy-basic import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")
```

## 14.3 資料庫連線

設定資料庫連線配置。

[程式檔案：14-3-database-connection.py](../_code/14/14-3-database-connection.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 14.4 CRUD 操作

實作基本的資料庫 CRUD 操作。

[程式檔案：14-4-crud-operations.py](../_code/14/14-4-crud-operations.py)

```python
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
```

## 14.5 SQLite 範例

SQLite 是輕量級的檔案型資料庫。

[程式檔案：14-5-sqlite-demo.py](../_code/14/14-5-sqlite-demo.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./sqlite.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class DemoModel(Base):
    __tablename__ = "demo"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

Base.metadata.create_all(bind=engine)

def demo_operations():
    db = SessionLocal()
    try:
        demo = DemoModel(name="Test")
        db.add(demo)
        db.commit()
        print("Created:", demo.name)
        
        results = db.query(DemoModel).all()
        print("All records:", results)
    finally:
        db.close()

if __name__ == "__main__":
    demo_operations()
```

## 14.6 PostgreSQL 範例

PostgreSQL 是功能強大的開源關聯式資料庫。

[程式檔案：14-6-postgres-demo.py](../_code/14/14-6-postgres-demo.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_URL = "postgresql://user:password@localhost:5432/mydb"

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class DemoModel(Base):
    __tablename__ = "demo"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 14.7 資料庫遷移

使用 Alembic 管理資料庫遷移。

[程式檔案：14-7-migration.py](../_code/14/14-7-migration.py)

```python
from sqlalchemy import create_engine, inspect
from alembic.config import Config
from alembic import command

engine = create_engine("sqlite:///./app.db")

def create_migration():
    alembic_cfg = Config("alembic.ini")
    command.init(alembic_cfg, "migrations")
    
def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def rollback_migration():
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, "-1")

def show_tables():
    inspector = inspect(engine)
    return inspector.get_table_names()

if __name__ == "__main__":
    print("Tables:", show_tables())
```

## 14.8 關聯關係

設定表之間的關聯。

[程式檔案：14-8-relationships.py](../_code/14/14-8-relationships.py)

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from 14-1-sqlalchemy-basic import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")
```

## 14.9 進階查詢

使用 SQLAlchemy 進行複雜查詢。

[程式檔案：14-9-query-params.py](../_code/14/14-9-query-params.py)

```python
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
```

## 14.10 交易處理

確保資料庫操作的原子性。

[程式檔案：14-10-transaction.py](../_code/14/14-10-transaction.py)

```python
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
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| SQLAlchemy | Python ORM 工具 |
| declarative_base | 定義模型基類 |
| sessionmaker | 建立資料庫 session |
| relationship | 表之間的關聯 |
| CRUD | Create, Read, Update, Delete |
| 交易 | 確保資料一致性 |

## 練習題

1. 建立一個部落格系統的資料庫模型
2. 實作文章和分類的多對多關係
3. 建立使用者認證相關的資料表
4. 實作資料庫遷移流程
