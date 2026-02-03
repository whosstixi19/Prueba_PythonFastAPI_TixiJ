from ast import In
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from .database import Base
from sqlalchemy.orm import relationship

class Vehiculo(Base):
    __tablename__ = "vehiculo"

    placa = Column(String(10), primary_key=True, index=True, nullable=False)
    propietario = Column(String(100), index=True, nullable=False)
    marca = Column(String(50), index=True, nullable=False)
    fabricacion = Column(Integer, index=True, nullable=False)
    valor_comercial = Column(Float, index=True, nullable=True)

    #A tributos calculados
    impuesto = Column(Float, index=True, nullable=True)
    codigo_revision= Column(String(20), index=True, nullable=True)
