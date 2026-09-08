# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# কোনো পাসওয়ার্ড বা কনফিগারেশন ঝামেলা ছাড়া সরাসরি লোকাল ডেটাবেজ ফাইল
DATABASE_URL = "sqlite:///./skillnest.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()