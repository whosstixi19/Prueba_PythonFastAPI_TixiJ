from typing import List, Optional
from pydantic import BaseModel

class VehiculoBase(BaseModel):
    placa: str
    propietario: str
    marca: str
    fabricacion: int
    valor_comercial: float
    impuesto: Optional[float] = None
    codigo_revision: Optional[str] = None

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    
    class Config:
        from_attributes = True