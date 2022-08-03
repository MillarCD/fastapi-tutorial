from pydantic import BaseModel
from datetime import date


## Tipo de evaluaciones
class EvaluationType(BaseModel):
    type_name: str
    class Config:
        orm_mode = True


## Evaluaciones
class EvaluationBase(BaseModel):
    id_eva: str
    name: str
    value: float | None = None
    eval_date: date | None = None
    evaluation_type: str
    
class EvaluationCreate(EvaluationBase):
    pass

class Evaluation(EvaluationBase):
    note: float | None = None

    class Config:
        orm_mode = True


## asignaturas
class CourseBase(BaseModel): # modelo base
    name: str
    code: str

class CourseCreate(CourseBase): # modelo con los datos que entrega el usuario
    class Config:
        orm_mode = True

class Course(CourseBase): # modelo que se retorna
    evaluations: list[Evaluation] = []

    class Config:
        orm_mode = True

