from sqlalchemy.orm import Session

from . import models, schemas

def get_courses(db: Session):
    courses = db.query(models.Course).all()
    return courses

def get_course(db: Session, code: str):
    return db.query(models.Course).filter(models.Course.code==code).first()

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(code=course.code, name=course.name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def get_evaluations(db: Session, course_code: str):
    return db.query(models.Evaluation).filter(models.Evaluation.code==course_code).all()


def create_evaluation(db: Session, course_code: str, evaluation: schemas.EvaluationCreate):

    db_evaluation = models.Evaluation( **evaluation.dict(), code=course_code )

    db.add(db_evaluation )
    db.commit()
    db.refresh(db_evaluation)

    return db_evaluation
