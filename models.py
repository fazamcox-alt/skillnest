# models.py
from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    whatsapp_number = Column(String(20), nullable=True)
    base_commission_percent = Column(Float, default=30.0)
    created_at = Column(DateTime, server_default=func.now())

    batches = relationship("Batch", back_populates="teacher")


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    max_seats = Column(Integer, default=20)  # ২০ জন হলেই ব্যাচ অটো-লক
    is_locked = Column(Boolean, default=False)
    class_days = Column(String(100), default="Sun, Tue, Thu")
    class_time = Column(String(50), default="09:00 PM")
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    teacher = relationship("Teacher", back_populates="batches")
    students = relationship("Student", back_populates="batch")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    guardian_name = Column(String(120), nullable=True)
    guardian_phone = Column(String(20), index=True, nullable=True)
    date_of_birth = Column(Date, nullable=True)

    # লজিস্টিকস ও পোশাকের পরিমাপ
    height_inches = Column(Integer, nullable=True)
    chest_size_inches = Column(Integer, nullable=True)
    tshirt_size = Column(String(10), default="M")
    kit_dispatch_status = Column(String(30), default="Pending")  # Pending, Shipped, Delivered

    # শোকেস ও ক্লাউড ব্যাকআপ রেফারেন্স (জিরো স্টোরেজ পলিসি)
    baseline_video_url = Column(String(500), nullable=True)
    archive_drive_id = Column(String(255), nullable=True)

    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    batch = relationship("Batch", back_populates="students")
    daily_logs = relationship("DailyLifeLog", back_populates="student")


class DailyLifeLog(Base):
    __tablename__ = "daily_life_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    log_date = Column(Date, server_default=func.current_date(), index=True)
    sleep_hours = Column(Float, nullable=False)
    dopamine_detox_passed = Column(Boolean, default=True)  # স্ক্রিনটাইম ও রিলস নিয়ন্ত্রণ
    practiced_two_hours = Column(Boolean, default=True)    # দৈনিক ২ ঘণ্টার প্র্যাকটিস
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="daily_logs")