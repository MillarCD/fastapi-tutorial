from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/courses/', response_model=list[schemas.Course]) 
def read_courses(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db)
    return courses

@app.post('/course/', response_model=schemas.CourseCreate)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, code=course.code)
    if db_course:
        raise HTTPException(status_code=400, detail='Asignatura ya registrada')
    return crud.create_course(db=db, course=course)


@app.get('/{course_code}/evaluations/', response_model=list[schemas.Evaluation])
def read_evaluations(course_code: str, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, code=course_code)
    if not db_course:
        raise HTTPException(status_code=400, detail='Asignatura no registrada')
    return crud.get_evaluations(db, course_code)

@app.post('/{course_code}/evaluation/', response_model=schemas.Evaluation)
def create_evaluations(course_code: str, evaluation: schemas.EvaluationCreate, db: Session = Depends(get_db)):
    return crud.create_evaluation(db, course_code, evaluation)
