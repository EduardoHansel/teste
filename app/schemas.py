from pydantic import BaseModel, Field
from datetime import date, time
from typing import List, Optional

# ----------- SCHEMAS PARA BLOCOS -----------
class BlocoBase(BaseModel):
    curso_id: int
    nome: str = Field(..., max_length=100)

class BlocoCreate(BlocoBase):
    pass

class Bloco(BlocoBase):
    id: int

    class Config:
        from_attributes = True

# ----------- SCHEMAS PARA SALAS -----------
class SalaBase(BaseModel):
    bloco_id: int
    numero: int = Field(..., gt=0)
    capacidade: int = Field(..., gt=0)
    recursos: str = Field(..., max_length=100)
    exclusivo: bool

class SalaCreate(SalaBase):
    pass

class Sala(SalaBase):
    id: int

    class Config:
        from_attributes = True

# ----------- SCHEMAS PARA COORDENADORES -----------
class CoordenadorBase(BaseModel):
    curso_id: int
    nome: str = Field(..., max_length=100)
    email: str
    senha: str = Field(..., max_length=100)

class CoordenadorCreate(CoordenadorBase):
    pass

class Coordenador(CoordenadorBase):
    id: int

    class Config:
        from_attributes = True

# ----------- SCHEMAS PARA RESERVAS -----------
class ReservaBase(BaseModel):
    sala_id: int
    coordenador_id: int
    data_reserva: date
    hora_inicio: time
    hora_fim: time
    motivo: str = Field(..., max_length=100)

class ReservaCreate(ReservaBase):
    pass

class Reserva(ReservaBase):
    id: int

    class Config:
        from_attributes = True

# ----------- SCHEMAS PARA CURSOS -----------
class CursoBase(BaseModel):
    nome: str = Field(..., max_length=100)

class CursoCreate(CursoBase):
    pass

class Curso(CursoBase):
    id: int

    class Config:
        from_attributes = True
