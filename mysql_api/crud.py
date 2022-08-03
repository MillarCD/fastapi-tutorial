from sqlalchemy.orm import Session

from . import models, schemas

def get_courses(db: Session):
    courses = db.query(models.Course).all()
    return courses


# def get_evaluations(db: Session, course_name: str):
#     course= db.query(models.Course).filter(models.Course.name==course_name).all()
#     print('course: ',course)
#     course_code = course.code
#     print('course_code: ', course_code)
#     return db.query(models.Evaluation).filter(models.Evaluations.course_code==course_code)
