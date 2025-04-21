from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, crud, database
from app.lista_doble import ListaDoblementeEnlazada

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Gestión de Vuelos")

lista_vuelos = ListaDoblementeEnlazada()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. POST /vuelos/ - Crear vuelo en BD y lista
@app.post("/vuelos/", response_model=schemas.VueloOut)
def crear_vuelo(vuelo: schemas.VueloCreate, db: Session = Depends(get_db)):
    nuevo = crud.crear_vuelo(db, vuelo)
    if vuelo.prioridad.lower() == "emergencia":
        lista_vuelos.insertar_al_frente(nuevo)
    else:
        lista_vuelos.insertar_al_final(nuevo)
    return nuevo

# 2. POST /vuelos/insertar-posicion/{posicion} - Insertar vuelo en posición específica
@app.post("/vuelos/insertar-posicion/{posicion}")
def insertar_vuelo_posicion(posicion: int, vuelo: schemas.VueloCreate):
    lista_vuelos.insertar_en_posicion(vuelo, posicion)
    return {
        "mensaje": f"Vuelo insertado en la posición {posicion}",
        "vuelo": vuelo
    }

# 3. GET /vuelos/ - Obtener todos los vuelos desde la base de datos
@app.get("/vuelos/", response_model=list[schemas.VueloOut])
def obtener_vuelos(db: Session = Depends(get_db)):
    return crud.obtener_vuelos(db)

# 4. GET /vuelos/{id} - Obtener un vuelo por ID
@app.get("/vuelos/{id}", response_model=schemas.VueloOut)
def obtener_vuelo_id(id: int, db: Session = Depends(get_db)):
    vuelo = db.query(models.Vuelo).filter(models.Vuelo.id == id).first()
    if vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return vuelo

# 5. GET /vuelos/longitud - Obtener número total de vuelos en lista enlazada
@app.get("/vuelos/longitud")
def obtener_longitud():
    return {"longitud": lista_vuelos.longitud()}

# 6. GET /vuelos/ultimo - Obtener el último vuelo de la lista enlazada
@app.get("/vuelos/ultimo")
def obtener_ultimo():
    vuelo = lista_vuelos.obtener_ultimo()
    if vuelo is None:
        raise HTTPException(status_code=404, detail="No hay vuelos en la lista")
    return vuelo

# 7. DELETE /vuelos/{id} - Eliminar vuelo de la base de datos
@app.delete("/vuelos/{id}")
def eliminar_vuelo(id: int, db: Session = Depends(get_db)):
    exito = crud.eliminar_vuelo(db, id)
    if not exito:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return {"mensaje": f"Vuelo con ID {id} eliminado"}

# 8. PATCH /vuelos/{id} - Actualizar parcialmente un vuelo
@app.patch("/vuelos/{id}", response_model=schemas.VueloOut)
def actualizar_vuelo(id: int, vuelo_actualizado: schemas.VueloCreate, db: Session = Depends(get_db)):
    vuelo = db.query(models.Vuelo).filter(models.Vuelo.id == id).first()
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")

    vuelo.codigo = vuelo_actualizado.codigo
    vuelo.destino = vuelo_actualizado.destino
    vuelo.prioridad = vuelo_actualizado.prioridad
    db.commit()
    db.refresh(vuelo)
    return vuelo
