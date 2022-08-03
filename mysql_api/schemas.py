from pydantic import BaseModel
from datetime import date

## Tipo de evaluaciones

class EvaluationsTypes(BaseModel):
    name: str
    class Config:
        orm_mode = True

## Evaluaciones

class EvaluationsBase(BaseModel):
    name: str
    value: float | None = None
    eval_date: date | None = None
    type: EvaluationsTypes
    
class EvaluationsCreate(EvaluationsBase):
    pass

class Evaluations(EvaluationsBase):
    note: float | None = None

    class Config:
        orm_mode = True

## asignaturas
class CourseBase(BaseModel): # modelo base
    name: str
    code: str

class CourseCreate(CourseBase): # modelo con los datos que entrega el usuario
    pass

class Course(CourseBase): # modelo que se retorna
    evaluations: list[Evaluations] | None = None

    class Config:
        orm_mode = True


