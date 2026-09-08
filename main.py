# main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List

from database import init_db, get_db
import models
import algorithms

app = FastAPI(
    title="SkillNest Core API",
    description="Enterprise API Engine for SkillNest Management Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/", response_class=FileResponse)
def read_index():
    if os.path.exists("index.html"):
        return "index.html"
    return {"message": "index.html file not found"}

# --- Pydantic Schemas ---
class StudentAdmissionSchema(BaseModel):
    full_name: str
    phone: str
    guardian_phone: Optional[str] = None
    height_inches: Optional[int] = None
    chest_size_inches: Optional[int] = None
    tshirt_size: str = Field(default="M")
    batch_id: Optional[int] = None

# --- API Endpoints ---

@app.get("/api/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "active", "service": "SkillNest API Engine"}

# সব স্টুডেন্টদের তালিকা ও লজিস্টিকস দেখার এন্ডপয়েন্ট
@app.get("/api/students")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).order_by(models.Student.id.desc()).all()
    return students

@app.post("/api/students/admit", status_code=status.HTTP_201_CREATED)
def admit_student(payload: StudentAdmissionSchema, db: Session = Depends(get_db)):
    existing_student = db.query(models.Student).filter(models.Student.phone == payload.phone).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="এই ফোন নম্বরে ইতিমধ্যে শিক্ষার্থী ভর্তি আছে।")

    new_student = models.Student(
        full_name=payload.full_name,
        phone=payload.phone,
        guardian_phone=payload.guardian_phone,
        height_inches=payload.height_inches,
        chest_size_inches=payload.chest_size_inches,
        tshirt_size=payload.tshirt_size,
        batch_id=payload.batch_id,
        kit_dispatch_status="Pending"
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student admitted successfully.",
        "student_id": new_student.id,
        "dispatch_status": new_student.kit_dispatch_status
    }