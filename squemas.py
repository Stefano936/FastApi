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


#Aca lo que hay que poner es que se agregue el resto de metodos que faltan y hay que modificar el models