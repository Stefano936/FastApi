from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy import text
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Actividades, Equipamiento, Instructores, Clase, AlumnoClase, Turnos, Alumnos, User
from squemas import ActividadCreate, EquipamientoCreate, ActividadModify, EquipamientoModify, TurnoCreate, TurnoModify, InstructorCreate, InstructorModify
from squemas import ClaseCreate, ClaseModify, AlumnoCreate, AlumnoModify, AlumnoClaseCreate, AlumnoClaseModify, LoginRequest

app = FastAPI()     
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
#                            Alumnos                                 #
######################################################################

#Get para obtener alumnos
@app.get("/alumnos")
async def get_alumnos(db: Session = Depends(get_db)):
    query_alumnos = text("SELECT * FROM alumnos")
    result = db.execute(query_alumnos).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No alumnos found")
    
    alumnos = []
    for row in result:
        alumno = {
            "ci": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "telefono": row[3],
            "fecha_nacimiento": row[4],
            "correo": row[5]
        }
        alumnos.append(alumno)
        
    return alumnos

#Post para subir alumnos
@app.post("/alumnos")
async def create_alumnos(alumnos: AlumnoCreate, db: Session = Depends(get_db)):
    query_insert = text("""
        INSERT INTO alumnos (ci, nombre, apellido, telefono, fecha_nacimiento, correo)
        VALUES (:ci, :nombre, :apellido, :telefono, :fecha_nacimiento, :correo)
    """)
    db.execute(query_insert, {
        "ci": alumnos.ci,
        "nombre": alumnos.nombre,
        "apellido": alumnos.apellido,
        "telefono": alumnos.telefono,
        "fecha_nacimiento": alumnos.fecha_nacimiento,
        "correo": alumnos.correo
    })
    db.commit()
    
    query_alumno = text("SELECT * FROM alumnos WHERE ci = :ci")
    result = db.execute(query_alumno, {"ci": alumnos.ci}).fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="Alumno not found after creation")
    
    alumno = {
        "ci": result[0],
        "nombre": result[1],
        "apellido": result[2],
        "telefono": result[3],
        "fecha_nacimiento": result[4],
        "correo": result[5]
    }
    
    return alumno

#Put para modificar alumnos
@app.put("/alumnos/{ci}")
async def update_alumnos(ci: str, alumnos: dict, db: Session = Depends(get_db)):
    print(alumnos)
    query_alumnos = text("SELECT * FROM alumnos WHERE ci = :ci")
    result = db.execute(query_alumnos, {"ci": ci}).fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="Alumno not found")
    
    query_update = text("""
        UPDATE alumnos
        SET nombre = :nombre, apellido = :apellido,  fecha_nacimiento = :fecha_nacimiento,telefono = :telefono, correo = :correo
        WHERE ci = :ci
    """)
    db.execute(query_update, {
        "nombre": alumnos.get("nombre"),
        "apellido": alumnos.get("apellido"),
        "telefono": alumnos.get("telefono"),
        "fecha_nacimiento": alumnos.get("fecha_nacimiento"),
        "correo": alumnos.get("correo"),
        "ci": alumnos.get("ci")
    })
    db.commit()
    
    query_alumno = text("SELECT * FROM alumnos WHERE ci = :ci")
    result = db.execute(query_alumno, {"ci": ci}).fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="Alumno not found after update")
    
    alumno = {
        "ci": result[0],
        "nombre": result[1],
        "apellido": result[2],
        "telefono": result[3],
        "fecha_nacimiento": result[4],
        "correo": result[5]
    }
    
    return alumno

#Delete para borrar alumnos
@app.delete("/alumnos/{ci}")
async def delete_alumnos(ci: str, db: Session = Depends(get_db)):
    query_alumnos = text(f"SELECT * FROM alumnos WHERE ci = {ci}")
    result = db.execute(query_alumnos).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Alumno not found")

    query_delete = text(f"DELETE FROM alumnos WHERE ci = {ci}")
    db.execute(query_delete)
    db.commit()
    return {"message": "Alumno deleted successfully"}

#En vez de filter tenemos que usar el query, select algo from tabla ta

######################################################################
#                           Registro                                 #
######################################################################

######################################################################
#                            Login                                   #
######################################################################

@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.ci == request.ci).first()
    if user and user.contraseña == request.contraseña:
        return {"message": "Login successful", "correo": user.correo}
    else:
        raise HTTPException(status_code=401, detail="Invalid CI or password")
    
######################################################################
#                            Alumnosclase                            #
######################################################################

#Get para obtener alumnosclase
@app.get("/alumnosclase")
async def get_alumnosclase(db: Session = Depends(get_db)):
    alumnosclase = db.query(AlumnoClase).all()
    if not alumnosclase:
        raise HTTPException(status_code=404, detail="No alumnosclase found")
    return alumnosclase

#Post para subir alumnosclase, para poder hacer un post tengo que modificar la tabla de alumnos ci_alumnos
@app.post("/alumnosclase")
async def create_alumnosclase(alumnosclase: AlumnoClaseCreate, db: Session = Depends(get_db)):
    nuevoAlumnoClase = AlumnoClase(id_clase=alumnosclase.id_clase, ci=alumnosclase.ci, id_equipamiento=alumnosclase.id_equipamiento)
    db.add(nuevoAlumnoClase)
    db.commit()
    db.refresh(nuevoAlumnoClase)
    return nuevoAlumnoClase 

#Put para modificar alumnosclase
@app.put("/alumnosclase/{id_clase}/{ci}/{id_equipamiento}")
async def update_alumnosclase(id_clase: int, ci: str, id_equipamiento: int, alumnosclase: AlumnoClaseModify, db: Session = Depends(get_db)):
    db_alumnosclase = db.query(AlumnoClase).filter(AlumnoClase.id_clase == id_clase, AlumnoClase.ci == ci, AlumnoClase.id_equipamiento == id_equipamiento).first()
    if not db_alumnosclase:
        raise HTTPException(status_code=404, detail="AlumnoClase not found")
    db_alumnosclase.id_clase = alumnosclase.id_clase
    db_alumnosclase.ci = alumnosclase.ci
    db_alumnosclase.id_equipamiento = alumnosclase.id_equipamiento
    db.commit()
    db.refresh(db_alumnosclase)
    return db_alumnosclase

#Delete para borrar alumnosclase
@app.delete("/alumnosclase/{id_clase}/{ci}/{id_equipamiento}")
async def delete_alumnosclase(id_clase: int, ci: str, id_equipamiento: int, db: Session = Depends(get_db)):
    db_alumnosclase = db.query(AlumnoClase).filter(AlumnoClase.id_clase == id_clase, AlumnoClase.ci == ci, AlumnoClase.id_equipamiento == id_equipamiento).first()
    if not db_alumnosclase:
        raise HTTPException(status_code=404, detail="AlumnoClase not found")
    db.delete(db_alumnosclase)
    db.commit()
    return {"message": "AlumnoClase deleted successfully"}