from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)
    print("Las tablas de la base de datos han sido creadas (si no existían).")

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a tu API Vehicular con FastAPI!/ Jose Tixi"}


# Leer todas los vehiculos
@app.get("/api/vehiculos", response_model=List[schemas.Vehiculo])
def read_vehiculos(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    vehiculos = db.query(models.Vehiculo).offset(skip).limit(limit).all()
    return vehiculos
# Leer una VEHICULO por PLACA
@app.get("/api/vehiculos/{placa}", response_model=schemas.Vehiculo)
def read_vehiculo(placa: str, db: Session = Depends(database.get_db)):
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.placa == placa).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Placa no encontrada")
    return db_vehiculo

# Crear un nuevo Vehículo
@app.post("/api/vehiculos", response_model=schemas.Vehiculo)
def create_vehiculo(vehiculo: schemas.VehiculoCreate, db: Session = Depends(database.get_db)):

    # Verificar si ya existe un vehículo con la misma placa
    db_vehiculo_existente = db.query(models.Vehiculo).filter(models.Vehiculo.placa == vehiculo.placa).first()
    if db_vehiculo_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un vehículo con esta placa")
    
    db_vehiculo = models.Vehiculo(**vehiculo.dict())
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

# Actualizar un Vehículo
@app.put("/api/vehiculos", response_model=schemas.Vehiculo)
def update_vehiculo(vehiculo: schemas.Vehiculo, db: Session = Depends(database.get_db)):
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.placa == vehiculo.placa).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehículo no encontrado")
    
    db_vehiculo.propietario = vehiculo.propietario
    db_vehiculo.marca = vehiculo.marca
    db_vehiculo.fabricacion = vehiculo.fabricacion
    db_vehiculo.valor_comercial = vehiculo.valor_comercial
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

# Eliminar un Vehículo
@app.delete("/api/vehiculos/{placa}")
def delete_vehiculo(placa: str, db: Session = Depends(database.get_db)):
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.placa == placa).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehículo no encontrado")
    
    db.delete(db_vehiculo)
    db.commit()
    return {"message": "Vehículo eliminado exitosamente"}