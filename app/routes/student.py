from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentLogin
from app.utils.security import hash_password, verify_password

router = APIRouter(prefix="/student", tags=["Student"])


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Register Student
@router.post("/register")
def register_student(data: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(
        Student.university_roll_number == data.university_roll_number
    ).first()

    if existing:
        return {"error": "Student already exists"}

    student = Student(
        university_roll_number=data.university_roll_number,
        full_name=data.full_name,
        branch=data.branch,
        cgpa=data.cgpa,
        batch=data.batch,
        password_hash=hash_password(data.password)
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {"message": "Student registered successfully", "student_id": student.id}


# ✅ Login Student
@router.post("/login")
def login_student(data: StudentLogin, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        Student.university_roll_number == data.university_roll_number
    ).first()

    if not student:
        return {"error": "Student not found"}

    if not verify_password(data.password, student.password_hash):
        return {"error": "Invalid password"}

    return {"message": "Login successful", "student_id": student.id}


# ✅ View Student Profile
@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        return {"error": "Student not found"}

    return student


# ✅ View All Students (Admin use)
@router.get("/")
def view_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

# ✅ Update Student Profile
@router.put("/{student_id}")
def update_student(student_id: int, data: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        return {"error": "Student not found"}

    # Prevent changing roll number
    update_data = data.dict()
    update_data.pop("university_roll_number", None)

    for key, value in update_data.items():
        if key == "password":
            student.password_hash = hash_password(value)
        else:
            setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return {"message": "Student updated successfully"}