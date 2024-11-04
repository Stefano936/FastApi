from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Actividades
from models import Equipamiento
from models import Instructores
from models import Clase
from models import AlumnoClase

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/actividades")
async def get_actividades(db: Session = Depends(get_db)):
    actividades = db.query(Actividades).all()
    if not actividades:
        raise HTTPException(status_code=404, detail="No hay actividades")
    return actividades

@app.get("/equipamiento")
async def get_equipamiento(db: Session = Depends(get_db)):
    equipamiento = db.query(Equipamiento).all()
    if not equipamiento:
        raise HTTPException(status_code=404, detail="No equipment found")
    return equipamiento

@app.get("/instructores")
async def get_instructores(db: Session = Depends(get_db)):
    instructores = db.query(Instructores).all()
    if not instructores:
        raise HTTPException(status_code=404, detail="No instructors found")
    return instructores

#Revisar este que no anda
@app.get("/clases")
async def get_clases(db: Session = Depends(get_db)):
    clases = db.query(Clase).all()
    if not clases:
        raise HTTPException(status_code=404, detail="No classes found")
    return clases

#Revisar este que no anda
@app.get("/alumnosclase")
async def get_alumnosclase(db: Session = Depends(get_db)):
    alumnosclase = db.query(AlumnoClase).all()
    if not alumnosclase:
        raise HTTPException(status_code=404, detail="No alumnosclase found")
    return alumnosclase