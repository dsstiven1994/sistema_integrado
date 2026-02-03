from pydantic import BaseModel
from typing import Optional

class RequerimientoCreate(BaseModel):
    empresa_nit: str
    tipo_solicitud: str
    prioridad: str = "normal"
    descripcion: Optional[str] = ""

class RequerimientoUpdate(BaseModel):
    estado: str
    prioridad: str
    responsable_id: Optional[int]
    resolucion: Optional[str] = ""
