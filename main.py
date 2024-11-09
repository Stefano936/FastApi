from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Actividades, Equipamiento, Instructores, Clase, AlumnoClase, Turnos
from squemas import ActividadCreate, EquipamientoCreate, ActividadModify, EquipamientoModify, TurnoCreate, TurnoModify, InstructorCreate, InstructorModify
from squemas import ClaseCreate, ClaseModify, AlumnoClaseCreate, AlumnoClaseModify

app = FastAPI()     
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

######################################################################
#                            Actividades                             #
######################################################################

#Get para obtener actividades
@app.get("/actividades")
async def get_actividades(db: Session = Depends(get_db)):
    actividades = db.query(Actividades).all()
    if not actividades:
        raise HTTPException(status_code=404, detail="No hay actividades")
    return actividades

#Post para subir actividades
@app.post("/actividades")
async def create_actividades(actividades:ActividadCreate, db: Session = Depends(get_db)):
    nuevaActividad = Actividades(descripcion=actividades.descripcion, costo=actividades.costo)
    db.add(nuevaActividad)
    db.commit()
    db.refresh(nuevaActividad)
    return nuevaActividad

#Put para modificar actividades
@app.put("/actividades/{id}")
async def update_actividades(id: int, actividades: ActividadModify, db: Session = Depends(get_db)):
    db_actividades = db.query(Actividades).filter(Actividades.id == id).first()
    if not db_actividades:
        raise HTTPException(status_code=404, detail="Actividades not found")
    db_actividades.descripcion = actividades.descripcion
    db_actividades.costo = actividades.costo
    db.commit()
    db.refresh(db_actividades)
    return db_actividades

#Delete para borrar actividades
@app.delete("/actividades/{id}")
async def delete_actividades(id: int, db: Session = Depends(get_db)):
    db_actividades = db.query(Actividades).filter(Actividades.id == id).first()
    if not db_actividades:
        raise HTTPException(status_code=404, detail="Actividades not found")
    db.delete(db_actividades)
    db.commit()
    return {"message": "Actividades deleted successfully"}


######################################################################
#                            Equipamiento                            #
######################################################################
    
#Get para obtener equipamiento
@app.get("/equipamiento")
async def get_equipamiento(db: Session = Depends(get_db)):
    equipamiento = db.query(Equipamiento).all()
    if not equipamiento:
        raise HTTPException(status_code=404, detail="No equipment found")
    return equipamiento

#Post para subir equipamiento
@app.post("/equipamiento")
async def create_equipamiento(equipamiento:EquipamientoCreate, db: Session = Depends(get_db)):
    nuevoEquipamiento = Equipamiento(id_actividad=equipamiento.id_actividad,descripcion=equipamiento.descripcion, costo=equipamiento.costo)
    print(nuevoEquipamiento)
    db.add(nuevoEquipamiento)
    db.commit()
    db.refresh(nuevoEquipamiento)
    return nuevoEquipamiento

#Put para modificar equipamiento
@app.put("/equipamiento/{id}")
async def update_equipamiento(id: int, equipamiento: EquipamientoModify, db: Session = Depends(get_db)):
    db_equipamiento = db.query(Equipamiento).filter(Equipamiento.id == id).first()
    if not db_equipamiento:
        raise HTTPException(status_code=404, detail="Equipamiento not found")
    db_equipamiento.id_actividad = equipamiento.id_actividad
    db_equipamiento.descripcion = equipamiento.descripcion
    db_equipamiento.costo = equipamiento.costo
    db.commit()
    db.refresh(db_equipamiento)
    return db_equipamiento

#Delete para borrar equipamiento
@app.delete("/equipamiento/{id}")
async def delete_equipamiento(id: int, db: Session = Depends(get_db)):
    db_equipamiento = db.query(Equipamiento).filter(Equipamiento.id == id).first()
    if not db_equipamiento:
        raise HTTPException(status_code=404, detail="Equipamiento not found")
    db.delete(db_equipamiento)
    db.commit()
    return {"message": "Equipamiento deleted successfully"}


######################################################################
#                            Instructores                            #
######################################################################


#Get para obtener instructores
@app.get("/instructores")
async def get_instructores(db: Session = Depends(get_db)):
    instructores = db.query(Instructores).all()
    if not instructores:
        raise HTTPException(status_code=404, detail="No instructors found")
    return instructores

#Post para subir instructores
@app.post("/instructores")
async def create_instructores(instructores: InstructorCreate, db: Session = Depends(get_db)):
    nuevoInstructor = Instructores(ci=instructores.ci, nombre=instructores.nombre, apellido=instructores.apellido)
    db.add(nuevoInstructor)
    db.commit()
    db.refresh(nuevoInstructor)
    return nuevoInstructor

#Put para modificar instructores
@app.put("/instructores/{ci}")
async def update_instructores(ci: str, instructores: InstructorModify, db: Session = Depends(get_db)):
    db_instructores = db.query(Instructores).filter(Instructores.ci == ci).first()
    if not db_instructores:
        raise HTTPException(status_code=404, detail="Instructor not found")
    db_instructores.nombre = instructores.nombre
    db_instructores.apellido = instructores.apellido
    db.commit()
    db.refresh(db_instructores)
    return db_instructores

#Delete para borrar instructores
@app.delete("/instructores/{ci}")
async def delete_instructores(ci: str, db: Session = Depends(get_db)):
    db_instructores = db.query(Instructores).filter(Instructores.ci == ci).first()
    if not db_instructores:
        raise HTTPException(status_code=404, detail="Instructor not found")
    db.delete(db_instructores)
    db.commit()
    return {"message": "Instructor deleted successfully"}

######################################################################
#                            Clases                                  #
######################################################################

#Get para obtener clases
@app.get("/clases")
async def get_clases(db: Session = Depends(get_db)):
    clases = db.query(Clase).all()
    if not clases:
        raise HTTPException(status_code=404, detail="No classes found")
    return clases

#Post para subir clases
@app.post("/clases")
async def create_clases(clases: ClaseCreate, db: Session = Depends(get_db)):
    nuevaClase = Clase(ci_instructor=clases.ci_instructor, id_actividad=clases.id_actividad, id_turno=clases.id_turno, dictada=clases.dictada)
    db.add(nuevaClase)
    db.commit()
    db.refresh(nuevaClase)
    return nuevaClase

#Put para modificar clases
@app.put("/clases/{id}")
async def update_clases(id: int, clases: ClaseModify, db: Session = Depends(get_db)):
    db_clases = db.query(Clase).filter(Clase.id == id).first()
    if not db_clases:
        raise HTTPException(status_code=404, detail="Clase not found")
    db_clases.ci_instructor = clases.ci_instructor
    db_clases.id_actividad = clases.id_actividad
    db_clases.id_turno = clases.id_turno
    db_clases.dictada = clases.dictada
    db.commit()
    db.refresh(db_clases)
    return db_clases

#Delete para borrar clases
@app.delete("/clases/{id}")
async def delete_clases(id: int, db: Session = Depends(get_db)):
    db_clases = db.query(Clase).filter(Clase.id == id).first()
    if not db_clases:
        raise HTTPException(status_code=404, detail="Clase not found")
    db.delete(db_clases)
    db.commit()
    return {"message": "Clase deleted successfully"}

""""
######################################################################
#                            Alumnosclase                            #
######################################################################

#Revisar este que no anda
@app.get("/alumnosclase")
async def get_alumnosclase(db: Session = Depends(get_db)):
    alumnosclase = db.query(AlumnoClase).all()
    if not alumnosclase:
        raise HTTPException(status_code=404, detail="No alumnosclase found")
    return alumnosclase

"""

######################################################################
#                            Turnos                                  #
######################################################################

#Get para obtener turnos
@app.get("/turnos")
async def get_turnos(db: Session = Depends(get_db)):
    turnos = db.query(Turnos).all()
    if not turnos:
        raise HTTPException(status_code=404, detail="No turnos found")
    return turnos

#Post para subir turnos
@app.post("/turnos")
async def create_turnos(turnos: TurnoCreate, db: Session = Depends(get_db)):
    nuevoTurno = Turnos(hora_inicio=turnos.hora_inicio, hora_fin=turnos.hora_fin)
    db.add(nuevoTurno)
    db.commit()
    db.refresh(nuevoTurno)
    return nuevoTurno

#Put para modificar turnos
@app.put("/turnos/{id}")
async def update_turnos(id: int, turnos: TurnoModify, db: Session = Depends(get_db)):
    db_turnos = db.query(Turnos).filter(Turnos.id == id).first()
    if not db_turnos:
        raise HTTPException(status_code=404, detail="Turnos not found")
    db_turnos.hora_inicio = turnos.hora_inicio
    db_turnos.hora_fin = turnos.hora_fin
    db.commit()
    db.refresh(db_turnos)
    return db_turnos

#Delete para borrar turnos
@app.delete("/turnos/{id}")
async def delete_turnos(id: int, db: Session = Depends(get_db)):
    db_turnos = db.query(Turnos).filter(Turnos.id == id).first()
    if not db_turnos:
        raise HTTPException(status_code=404, detail="Turnos not found")
    db.delete(db_turnos)
    db.commit()
    return {"message": "Turnos deleted successfully"}

######################################################################
#                           Registro                                 #
######################################################################

######################################################################
#                            Login                                   #
######################################################################
