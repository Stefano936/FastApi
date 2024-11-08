from sqlalchemy import Column, Integer, String, Float, ForeignKey, CHAR, Boolean, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Actividades(Base):
    __tablename__ = "actividades"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)
    costo = Column(Float, nullable=False)

class Equipamiento(Base):
    __tablename__ = "equipamiento"
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    id_actividad = Column(Integer, ForeignKey('actividades.id'), nullable=False)
    descripcion = Column(String(255), nullable=False)
    costo = Column(Float, nullable=False)
    
    actividad = relationship("Actividades")

class Instructores(Base):
    __tablename__ = "instructores"
    
    ci = Column(CHAR(11), primary_key=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    correo = Column(String(255))

class Clase(Base):
    __tablename__ = "clase"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ci_instructor = Column(CHAR(11), ForeignKey('instructores.ci'), nullable=False)
    id_actividad = Column(Integer, ForeignKey('actividades.id'), nullable=False)
    id_turno = Column(Integer, ForeignKey('turnos.id'), nullable=False)
    dictada = Column(Boolean, default=False)
    
    instructor = relationship("Instructores")
    actividad = relationship("Actividades")
    turno = relationship("Turnos")

class AlumnoClase(Base):
    __tablename__ = "alumno_clase"
    
    id_clase = Column(Integer, ForeignKey('clase.id'), primary_key=True, nullable=False)
    ci_alumno = Column(CHAR(11), ForeignKey('alumnos.ci'), primary_key=True, nullable=False)
    id_equipamiento = Column(Integer, ForeignKey('equipamiento.id'), primary_key=True, nullable=False)

class Turnos(Base):
    __tablename__ = "turnos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)