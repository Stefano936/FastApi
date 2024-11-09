from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Actividades, Equipamiento, Instructores, Clase, AlumnoClase, Turnos
from squemas import ActividadCreate, EquipamientoCreate, ActividadModify, EquipamientoModify, TurnoCreate, TurnoModify

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

""""
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

######################################################################
#                            Clases                                  #
######################################################################

#Revisar este que no anda
@app.get("/clases")
async def get_clases(db: Session = Depends(get_db)):
    clases = db.query(Clase).all()
    if not clases:
        raise HTTPException(status_code=404, detail="No classes found")
    return clases

    
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
