from pydantic import BaseModel

class ActividadCreate(BaseModel):
    descripcion: str
    costo: float

