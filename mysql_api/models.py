from sqlalchemy import Column, ForeignKey, String, Float, Date
from sqlalchemy.orm import relationship

from .database import Base

class Course(Base):
    __tablename__ = 'Asignaturas'

    code = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)

    evaluations = relationship('Evaluation', back_populates='course')


class Evaluation(Base):
    __tablename__ = 'Evaluaciones'

    id_eva = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Float, index=True)
    eval_date = Column(Date, index=True)
    note = Column(Float, index=True)
    code = Column(String, ForeignKey('Asignaturas.code'))
    evaluation_type = Column(String, ForeignKey('Tipos_evaluaciones.type_name'))

    type_name = relationship('EvaluationType', back_populates='evaluations')
    course = relationship('Course', back_populates='evaluations')


class EvaluationType(Base):
    __tablename__ = 'Tipos_evaluaciones'

    type_name = Column(String, primary_key=True, index=True)

    evaluations = relationship('Evaluation', back_populates='type_name')
