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
