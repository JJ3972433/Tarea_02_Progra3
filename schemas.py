from pydantic import BaseModel

class VueloBase(BaseModel):
    codigo: str
    destino: str
    prioridad: str

class VueloCreate(VueloBase):
    pass

class VueloOut(VueloBase):
    id: int
    class Config:
        orm_mode = True
