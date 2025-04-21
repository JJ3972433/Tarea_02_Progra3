from sqlalchemy.orm import Session
from . import models, schemas

def crear_vuelo(db: Session, vuelo: schemas.VueloCreate):
    db_vuelo = models.Vuelo(**vuelo.dict())
    db.add(db_vuelo)
    db.commit()
    db.refresh(db_vuelo)
    return db_vuelo

def obtener_vuelos(db: Session):
    return db.query(models.Vuelo).all()

def eliminar_vuelo(db: Session, vuelo_id: int):
    vuelo = db.query(models.Vuelo).filter(models.Vuelo.id == vuelo_id).first()
    if vuelo:
        db.delete(vuelo)
        db.commit()
        return True
    return False
