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

# @app.post('/courses/', response_model=schemas.Course)
# def create_course(course: shemas.courseCreate, db: Session = Depends(get_db)):
#      return course

# @app.get('/{course}/evaluations/', response_model=list[schemas.Evaluations])
# def read_evaluations(course: str, db: Session = Depends(get_db)):
#     evaluations = crud.get_evaluations(db, course)
#     return evaluations

# @app.post('/{course}/evaluation/', response_model=schemas.Evaluations)
# def create_evaluations(course: str, evaluation: schemas.EvaluationsCreate, db: Session = Depends(get_db)):
#     return evaluation


