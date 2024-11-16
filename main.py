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
from datetime import timedelta


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
#                            Actividades                             #  PRONTAAA
######################################################################

#Get para obtener actividades
@app.get("/actividades")
async def get_actividades(db: Session = Depends(get_db)):
    query_actividades = text("SELECT * FROM actividades")
    result = db.execute(query_actividades).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No hay actividades")
    
    actividades = []
    
    for row in result:
        actividad = {
            "id": row[0],
            "descripcion": row[1],
            "costo": row[2]
        }
        actividades.append(actividad)
        
    return actividades

#Post para subir actividades
@app.post("/actividades")
async def create_actividades(actividades: dict, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO actividades (descripcion, costo)
        VALUES (:descripcion, :costo)
    """)
    db.execute(query, {
        "descripcion": actividades["descripcion"],
        "costo": actividades["costo"]
    })
    db.commit()
    
    # Obtener la actividad recién insertada
    query_last_inserted = text("""
        SELECT id, descripcion, costo
        FROM actividades
        WHERE id = (SELECT LAST_INSERT_ID())
    """)
    nuevaActividad = db.execute(query_last_inserted).fetchone()
    
    # Convertir la fila en un diccionario
    nuevaActividad_dict = {
        "id": nuevaActividad[0],
        "descripcion": nuevaActividad[1],
        "costo": nuevaActividad[2]
    }
    
    return nuevaActividad_dict

#Put para modificar actividades
@app.put("/actividades/{id}")
async def update_actividades(id: int, actividades: dict, db: Session = Depends(get_db)):
    # Verificar la existencia de la actividad
    query_actividades = text("SELECT id FROM actividades WHERE id = :id")
    result = db.execute(query_actividades, {"id": id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Actividades not found")
    
    # Actualizar la actividad
    query_update = text("""
        UPDATE actividades
        SET descripcion = :descripcion,
            costo = :costo
        WHERE id = :id
    """)
    db.execute(query_update, {
        "descripcion": actividades["descripcion"],
        "costo": actividades["costo"],
        "id": id
    })
    db.commit()
    
    # Obtener la actividad actualizada
    query_updated = text("""
        SELECT id, descripcion, costo
        FROM actividades
        WHERE id = :id
    """)
    updatedActividad = db.execute(query_updated, {"id": id}).fetchone()
    
    # Convertir la fila en un diccionario
    updatedActividad_dict = {
        "id": updatedActividad[0],
        "descripcion": updatedActividad[1],
        "costo": updatedActividad[2]
    }
    
    return updatedActividad_dict

@app.delete("/actividades/{id}")
async def delete_actividades(id: int, db: Session = Depends(get_db)):
    # Verificar la existencia de la actividad
    query_actividades = text("SELECT id FROM actividades WHERE id = :id")
    result = db.execute(query_actividades, {"id": id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Actividades not found")
    
    # Eliminar la actividad
    query_delete = text("DELETE FROM actividades WHERE id = :id")
    db.execute(query_delete, {"id": id})
    db.commit()
    
    return {"message": "Actividades deleted successfully"}

######################################################################
#                            Equipamiento                            #  PRONTAAA
######################################################################
    
#Get para obtener equipamiento
@app.get("/equipamiento")
async def get_equipamiento(db: Session = Depends(get_db)):
    query_equipamiento = text("SELECT * FROM equipamiento")
    result = db.execute(query_equipamiento).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No equipment found")
    
    equipamiento = []
    
    for row in result:
        equipo = {
            "id": row[0],
            "id_actividad": row[1],
            "descripcion": row[2],
            "costo": row[3]
        }
        equipamiento.append(equipo)
        
    return equipamiento


#Post para subir equipamiento
@app.post("/equipamiento")
async def create_equipamiento(equipamiento: dict, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO equipamiento (id_actividad, descripcion, costo)
        VALUES (:id_actividad, :descripcion, :costo)
    """)
    db.execute(query, {
        "id_actividad": equipamiento["id_actividad"],
        "descripcion": equipamiento["descripcion"],
        "costo": equipamiento["costo"]
    })
    db.commit()
    
    # Obtener el equipamiento recién insertado
    query_last_inserted = text("""
        SELECT id, id_actividad, descripcion, costo
        FROM equipamiento
        WHERE id = (SELECT LAST_INSERT_ID())
    """)
    nuevoEquipamiento = db.execute(query_last_inserted).fetchone()
    
    # Convertir la fila en un diccionario
    nuevoEquipamiento_dict = {
        "id": nuevoEquipamiento[0],
        "id_actividad": nuevoEquipamiento[1],
        "descripcion": nuevoEquipamiento[2],
        "costo": nuevoEquipamiento[3]
    }
    
    return nuevoEquipamiento_dict

#Put para modificar equipamiento
@app.put("/equipamiento/{id}")
async def update_equipamiento(id: int, equipamiento: dict, db: Session = Depends(get_db)):
    # Verificar la existencia del equipamiento
    query_equipamiento = text("SELECT id FROM equipamiento WHERE id = :id")
    result = db.execute(query_equipamiento, {"id": id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Equipamiento not found")
    
    # Actualizar el equipamiento
    query_update = text("""
        UPDATE equipamiento
        SET id_actividad = :id_actividad,
            descripcion = :descripcion,
            costo = :costo
        WHERE id = :id
    """)
    db.execute(query_update, {
        "id_actividad": equipamiento["id_actividad"],
        "descripcion": equipamiento["descripcion"],
        "costo": equipamiento["costo"],
        "id": id
    })
    db.commit()
    
    # Obtener el equipamiento actualizado
    query_updated = text("""
        SELECT id, id_actividad, descripcion, costo
        FROM equipamiento
        WHERE id = :id
    """)
    updatedEquipamiento = db.execute(query_updated, {"id": id}).fetchone()
    
    # Convertir la fila en un diccionario
    updatedEquipamiento_dict = {
        "id": updatedEquipamiento[0],
        "id_actividad": updatedEquipamiento[1],
        "descripcion": updatedEquipamiento[2],
        "costo": updatedEquipamiento[3]
    }
    
    return updatedEquipamiento_dict

#Delete para borrar equipamiento
@app.delete("/equipamiento/{id}")
async def delete_equipamiento(id: int, db: Session = Depends(get_db)):
    # Verificar la existencia del equipamiento
    query_equipamiento = text("SELECT id FROM equipamiento WHERE id = :id")
    result = db.execute(query_equipamiento, {"id": id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Equipamiento not found")
    
    # Eliminar el equipamiento
    query_delete = text("DELETE FROM equipamiento WHERE id = :id")
    db.execute(query_delete, {"id": id})
    db.commit()
    
    return {"message": "Equipamiento deleted successfully"}


######################################################################
#                            Instructores                            # PRONTAAA
######################################################################


#Get para obtener instructores
@app.get("/instructores")
async def get_instructores(db: Session = Depends(get_db)):
    query_instructores = text("SELECT * FROM instructores")
    result = db.execute(query_instructores).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No instructors found")
    
    instructores = []
    
    for row in result:
        instructor = {
            "ci": row[0],
            "nombre": row[1],
            "apellido": row[2]
        }
        instructores.append(instructor)
        
    return instructores

#Post para subir instructores
@app.post("/instructores")
async def create_instructores(instructores: dict, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO instructores (ci, nombre, apellido)
        VALUES (:ci, :nombre, :apellido)
    """)
    db.execute(query, {
        "ci": instructores["ci"],
        "nombre": instructores["nombre"],
        "apellido": instructores["apellido"]
    })
    db.commit()
    
    # Obtener el instructor recién insertado
    query_last_inserted = text("""
        SELECT ci, nombre, apellido
        FROM instructores
        WHERE ci = :ci
    """)
    nuevoInstructor = db.execute(query_last_inserted, {"ci": instructores["ci"]}).fetchone()
    
    # Convertir la fila en un diccionario
    nuevoInstructor_dict = {
        "ci": nuevoInstructor[0],
        "nombre": nuevoInstructor[1],
        "apellido": nuevoInstructor[2]
    }
    
    return nuevoInstructor_dict

#Put para modificar instructores
@app.put("/instructores/{ci}")
async def update_instructores(ci: str, instructores: dict, db: Session = Depends(get_db)):
    # Verificar la existencia del instructor
    query_instructor = text("SELECT ci FROM instructores WHERE ci = :ci")
    result = db.execute(query_instructor, {"ci": ci}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    # Actualizar el instructor
    query_update = text("""
        UPDATE instructores
        SET nombre = :nombre,
            apellido = :apellido
        WHERE ci = :ci
    """)
    db.execute(query_update, {
        "nombre": instructores["nombre"],
        "apellido": instructores["apellido"],
        "ci": ci
    })
    db.commit()
    
    # Obtener el instructor actualizado
    query_updated = text("""
        SELECT ci, nombre, apellido
        FROM instructores
        WHERE ci = :ci
    """)
    updatedInstructor = db.execute(query_updated, {"ci": ci}).fetchone()
    
    # Convertir la fila en un diccionario
    updatedInstructor_dict = {
        "ci": updatedInstructor[0],
        "nombre": updatedInstructor[1],
        "apellido": updatedInstructor[2]
    }
    
    return updatedInstructor_dict

#Delete para borrar instructores
@app.delete("/instructores/{ci}")
async def delete_instructores(ci: str, db: Session = Depends(get_db)):
    # Verificar la existencia del instructor
    query_instructor = text("SELECT ci FROM instructores WHERE ci = :ci")
    result = db.execute(query_instructor, {"ci": ci}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    # Eliminar el instructor
    query_delete = text("DELETE FROM instructores WHERE ci = :ci")
    db.execute(query_delete, {"ci": ci})
    db.commit()
    
    return {"message": "Instructor deleted successfully"}

######################################################################
#                            Clases                                  #  PRONTAAA
######################################################################

#Get para obtener clases
@app.get("/clases")
async def get_clases(db: Session = Depends(get_db)):
    query_clases = text("SELECT * FROM clase")
    result = db.execute(query_clases).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No clases found")
    
    clases = []
    
    for row in result:
        clase = {
            "id": row[0],
            "ci_instructor": row[1],
            "id_actividad": row[2],
            "id_turno": row[3],
            "dictada": row[4]
        }
        clases.append(clase)
        
    return clases

#Post para subir clases
@app.post("/clases")
async def create_clases(clases: dict, db: Session = Depends(get_db)):
    # Verificar la existencia del ci_instructor
    query_instructor = text("SELECT ci FROM instructores WHERE ci = :ci_instructor")
    result = db.execute(query_instructor, {"ci_instructor": clases["ci_instructor"]}).fetchone()
    if not result:
        raise HTTPException(status_code=400, detail="Instructor not found")
    
    query = text("""
        INSERT INTO clase (ci_instructor, id_actividad, id_turno, dictada)
        VALUES (:ci_instructor, :id_actividad, :id_turno, :dictada)
    """)
    db.execute(query, {
        "ci_instructor": clases["ci_instructor"],
        "id_actividad": clases["id_actividad"],
        "id_turno": clases["id_turno"],
        "dictada": clases["dictada"]
    })
    db.commit()
    
    # Obtener la clase recién insertada
    query_last_inserted = text("""
        SELECT id, ci_instructor, id_actividad, id_turno, dictada
        FROM clase
        WHERE id = LAST_INSERT_ID()
    """)
    nuevaClase = db.execute(query_last_inserted).fetchone()
    
    # Convertir la fila en un diccionario
    nuevaClase_dict = {
        "id": nuevaClase[0],
        "ci_instructor": nuevaClase[1],
        "id_actividad": nuevaClase[2],
        "id_turno": nuevaClase[3],
        "dictada": nuevaClase[4]
    }
    
    return nuevaClase_dict

#Put para modificar clases
@app.put("/clases/{id}")
async def update_clases(id: int, clases: dict, db: Session = Depends(get_db)):
    # Verificar la existencia de la clase
    query_clase = text("SELECT id FROM clase WHERE id = :id")
    result = db.execute(query_clase, {"id": id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Clase not found")
    
    # Actualizar la clase
    query_update = text("""
        UPDATE clase
        SET ci_instructor = :ci_instructor,
            id_actividad = :id_actividad,
            id_turno = :id_turno,
            dictada = :dictada
        WHERE id = :id
    """)
    db.execute(query_update, {
        "ci_instructor": clases["ci_instructor"],
        "id_actividad": clases["id_actividad"],
        "id_turno": clases["id_turno"],
        "dictada": clases["dictada"],
        "id": id
    })
    db.commit()
    
    # Obtener la clase actualizada
    query_updated = text("""
        SELECT id, ci_instructor, id_actividad, id_turno, dictada
        FROM clase
        WHERE id = :id
    """)
    updatedClase = db.execute(query_updated, {"id": id}).fetchone()
    
    # Convertir la fila en un diccionario
    updatedClase_dict = {
        "id": updatedClase[0],
        "ci_instructor": updatedClase[1],
        "id_actividad": updatedClase[2],
        "id_turno": updatedClase[3],
        "dictada": updatedClase[4]
    }
    
    return updatedClase_dict

#Delete para borrar clases
@app.delete("/clases/{id}")
async def delete_clases(id: int, db: Session = Depends(get_db)):
    # Eliminar filas dependientes en alumno_clase
    query_alumno_clase = text("DELETE FROM alumno_clase WHERE id_clase = :id")
    db.execute(query_alumno_clase, {"id": id})
    
    # Eliminar la clase
    query_clases = text("SELECT * FROM clase WHERE id = :id")
    result = db.execute(query_clases, {"id": id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Clase not found")
    
    query = text("DELETE FROM clase WHERE id = :id")
    db.execute(query, {"id": id})
    db.commit()

    return {"message": "Clase deleted successfully"}

######################################################################
#                            Turnos                                  #  PRONTAAA
######################################################################

#Get para obtener turnos
@app.get("/turnos")
async def get_turnos(db: Session = Depends(get_db)):
    query_turnos = text("SELECT * FROM turnos")
    result = db.execute(query_turnos).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No turnos found")
    
    turnos = []
    
    for row in result:
        time_delta_inicio = row[1]
        time_delta_fin = row[2]

        hours_inicio, remainder_inicio = divmod(time_delta_inicio.seconds, 3600)
        minutes_inicio, seconds_inicio = divmod(remainder_inicio, 60)
        formatted_time_inicio = f"{hours_inicio:02d}:{minutes_inicio:02d}"

        hours_fin, remainder_fin = divmod(time_delta_fin.seconds, 3600)
        minutes_fin, seconds_fin = divmod(remainder_fin, 60)
        formatted_time_fin = f"{hours_fin:02d}:{minutes_fin:02d}"

        turno = {
            "id": row[0],
            "hora_inicio": formatted_time_inicio,
            "hora_fin": formatted_time_fin
        }
        turnos.append(turno)
        
    return turnos

#Post para subir turnos
@app.post("/turnos")
async def create_turnos(turnos: TurnoCreate, db: Session = Depends(get_db)):
    hora_inicio_parts = [int(part) for part in turnos.hora_inicio.split(":")]
    hora_fin_parts = [int(part) for part in turnos.hora_fin.split(":")]

    hora_inicio_timedelta = timedelta(hours=hora_inicio_parts[0], minutes=hora_inicio_parts[1])
    hora_fin_timedelta = timedelta(hours=hora_fin_parts[0], minutes=hora_fin_parts[1])

    nuevoTurno = Turnos(hora_inicio=hora_inicio_timedelta, hora_fin=hora_fin_timedelta)
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
    
    hora_inicio_parts = [int(part) for part in turnos.hora_inicio.split(":")]
    hora_fin_parts = [int(part) for part in turnos.hora_fin.split(":")]

    db_turnos.hora_inicio = timedelta(hours=hora_inicio_parts[0], minutes=hora_inicio_parts[1])
    db_turnos.hora_fin = timedelta(hours=hora_fin_parts[0], minutes=hora_fin_parts[1])
    
    db.commit()
    db.refresh(db_turnos)
    return db_turnos

#Delete para borrar turnos
@app.delete("/turnos/{id}")
async def delete_turnos(id: int, db: Session = Depends(get_db)):
    query_turnos = text("SELECT * FROM turnos WHERE id = :id")
    result = db.execute(query_turnos, {"id": id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Turnos not found")
    
    query = text("DELETE FROM turnos WHERE id = :id")
    db.execute(query, {"id": id})
    db.commit()

    return {"message": "Turno deleted successfully"}

######################################################################
#                            Alumnos                                 #  PRONTAAA
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
    query_alumnosclase = text("SELECT * FROM alumno_clase")
    result = db.execute(query_alumnosclase).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No alumnosclase found")
    
    alumnosclase = []
    for row in result:
        alumno_clase = {
            "id_clase": row[0],
            "ci": row[1],
            "id_equipamiento": row[2]
        }
        alumnosclase.append(alumno_clase)
        
    return alumnosclase

#Post para subir alumnosclase, para poder hacer un post tengo que modificar la tabla de alumnos ci_alumnos
@app.post("/alumnosclase")
async def create_alumnosclase(alumnosclase: dict, db: Session = Depends(get_db)):
    # Verificar si la entrada ya existe
    query_check = text("""
        SELECT * FROM alumno_clase
        WHERE id_clase = :id_clase AND ci = :ci AND id_equipamiento = :id_equipamiento
    """)
    existing_entry = db.execute(query_check, {
        "id_clase": alumnosclase["id_clase"],
        "ci": alumnosclase["ci"],
        "id_equipamiento": alumnosclase["id_equipamiento"]
    }).fetchone()
    
    if existing_entry:
        raise HTTPException(status_code=400, detail="Duplicate entry for alumno_clase")
    
    # Insertar la nueva entrada
    query_insert = text("""
        INSERT INTO alumno_clase (id_clase, ci, id_equipamiento)
        VALUES (:id_clase, :ci, :id_equipamiento)
    """)
    db.execute(query_insert, {
        "id_clase": alumnosclase["id_clase"],
        "ci": alumnosclase["ci"],
        "id_equipamiento": alumnosclase["id_equipamiento"]
    })
    db.commit()
    
    query_last_inserted = text("""
        SELECT id_clase, ci, id_equipamiento
        FROM alumno_clase
        WHERE id_clase = :id_clase AND ci = :ci AND id_equipamiento = :id_equipamiento
    """)
    nuevoAlumnoClase = db.execute(query_last_inserted, {
        "id_clase": alumnosclase["id_clase"],
        "ci": alumnosclase["ci"],
        "id_equipamiento": alumnosclase["id_equipamiento"]
    }).fetchone()
    
    if not nuevoAlumnoClase:
        raise HTTPException(status_code=404, detail="AlumnoClase not found after creation")
    
    alumno_clase_dict = {
        "id_clase": nuevoAlumnoClase[0],
        "ci": nuevoAlumnoClase[1],
        "id_equipamiento": nuevoAlumnoClase[2]
    }
    
    return alumno_clase_dict

#Put para modificar alumnosclase
@app.put("/alumnosclase/{id_clase}/{ci}/{id_equipamiento}")
async def update_alumnosclase(id_clase: int, ci: str, id_equipamiento: int, alumnosclase: dict, db: Session = Depends(get_db)):
    query_alumnosclase = text("""
        SELECT * FROM alumno_clase
        WHERE id_clase = :id_clase AND ci = :ci AND id_equipamiento = :id_equipamiento
    """)
    result = db.execute(query_alumnosclase, {
        "id_clase": id_clase,
        "ci": ci,
        "id_equipamiento": id_equipamiento
    }).fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="AlumnoClase not found")
    
    query_update = text("""
        UPDATE alumno_clase
        SET id_clase = :new_id_clase, ci = :new_ci, id_equipamiento = :new_id_equipamiento
        WHERE id_clase = :id_clase AND ci = :ci AND id_equipamiento = :id_equipamiento
    """)
    db.execute(query_update, {
        "new_id_clase": alumnosclase["id_clase"],
        "new_ci": alumnosclase["ci"],
        "new_id_equipamiento": alumnosclase["id_equipamiento"],
        "id_clase": id_clase,
        "ci": ci,
        "id_equipamiento": id_equipamiento
    })
    db.commit()
    
    query_updated = text("""
        SELECT id_clase, ci, id_equipamiento
        FROM alumno_clase
        WHERE id_clase = :id_clase AND ci = :ci AND id_equipamiento = :id_equipamiento
    """)
    updatedAlumnoClase = db.execute(query_updated, {
        "id_clase": alumnosclase["id_clase"],
        "ci": alumnosclase["ci"],
        "id_equipamiento": alumnosclase["id_equipamiento"]
    }).fetchone()
    
    if not updatedAlumnoClase:
        raise HTTPException(status_code=404, detail="AlumnoClase not found after update")
    
    updated_alumno_clase_dict = {
        "id_clase": updatedAlumnoClase[0],
        "ci": updatedAlumnoClase[1],
        "id_equipamiento": updatedAlumnoClase[2]
    }
    
    return updated_alumno_clase_dict

#Delete para borrar alumnosclase
@app.delete("/alumnosclase/{id_clase}/{ci}/{id_equipamiento}")
async def delete_alumnosclase(id_clase: int, ci: str, id_equipamiento: int, db: Session = Depends(get_db)):
    query_alumnosclase = text("""
        SELECT * FROM alumno_clase
        WHERE id_clase = :id_clase AND ci = :ci AND id_equipamiento = :id_equipamiento
    """)
    result = db.execute(query_alumnosclase, {
        "id_clase": id_clase,
        "ci": ci,
        "id_equipamiento": id_equipamiento
    }).fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="AlumnoClase not found")
    
    query_delete = text("""
        DELETE FROM alumno_clase
        WHERE id_clase = :id_clase AND ci = :ci AND id_equipamiento = :id_equipamiento
    """)
    db.execute(query_delete, {
        "id_clase": id_clase,
        "ci": ci,
        "id_equipamiento": id_equipamiento
    })
    db.commit()
    
    return {"message": "AlumnoClase deleted successfully"}