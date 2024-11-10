from pydantic import BaseModel

class ActividadCreate(BaseModel):
    descripcion: str
    costo: float

class ActividadModify(BaseModel):
    descripcion: str
    costo: float

class EquipamientoCreate(BaseModel):
    id_actividad: int
    descripcion: str
    costo: float

class EquipamientoModify(BaseModel):
    id_actividad: int
    descripcion: str
    costo: float

class InstructorCreate(BaseModel):
    ci: str
    nombre: str
    apellido: str

class InstructorModify(BaseModel):
    ci: str
    nombre: str
    apellido: str

class ClaseCreate(BaseModel):
    ci_instructor: str
    id_actividad: int
    id_turno: int
    dictada: bool

class ClaseModify(BaseModel):
    ci_instructor: str
    id_actividad: int
    id_turno: int
    dictada: bool

class TurnoCreate(BaseModel):
    hora_inicio: str
    hora_fin: str

class TurnoModify(BaseModel):
    hora_inicio: str
    hora_fin: str

class AlumnoCreate(BaseModel):
    ci: str
    nombre: str
    apellido: str
    telefono: str
    fecha_nacimiento: str
    correo : str

class AlumnoModify(BaseModel):
    ci: str
    nombre: str
    apellido: str
    telefono: str
    fecha_nacimiento: str
    correo : str

class AlumnoClaseCreate(BaseModel):
    id_clase: int
    ci_alumno: str
    id_equipamiento: int

class AlumnoClaseModify(BaseModel):
    id_clase: int
    ci_alumno: str
    id_equipamiento: int

#Aca lo que hay que poner es que se agregue el resto de metodos que faltan y hay que modificar el models