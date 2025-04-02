from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db

router = APIRouter(prefix="/salas", tags=["Salas"])

@router.post("/", response_model=schemas.Sala)
def create_sala(sala_data: schemas.SalaCreate, db: Session = Depends(get_db)):
    """Cria uma nova sala"""
    return crud.create_sala(db, sala_data)

@router.get("/", response_model=list[schemas.Sala])
def get_salas(db: Session = Depends(get_db)):
    """Consulta de todas as salas no banco de dados."""
    return db.query(models.Salas).all()

@router.get("/{sala_id}", response_model=schemas.Sala)
def get_sala(sala_id: int, db: Session = Depends(get_db)):
    """Consulta de uma sala específica."""
    sala = db.query(models.Salas).filter(models.Salas.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return sala


@router.put("/{sala_id}", response_model=schemas.Sala)
def update_sala(sala_id: int, sala_data: schemas.SalaCreate, db: Session = Depends(get_db)):
    """Altera/atualiza as informações de uma sala."""
    bloco = db.query(models.Blocos).filter(models.Blocos.id == sala_data.bloco_id).first()
    if not bloco:
        raise HTTPException(status_code=404, detail="Bloco não encontrado")

    sala = db.query(models.Salas).filter(models.Salas.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada")

    sala.numero = sala_data.numero
    sala.capacidade = sala_data.capacidade
    sala.recursos = sala_data.recursos
    sala.bloco_id = sala_data.bloco_id
    sala.curso_id = bloco.curso_id
    sala.exclusivo = sala_data.exclusivo
    db.commit()
    db.refresh(sala)
    return sala


@router.delete("/{sala_id}")
def delete_sala(sala_id: int, db: Session = Depends(get_db)):
    """Deleta uma sala."""
    sala = db.query(models.Salas).filter(models.Salas.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada")  # Corrigido aqui
    db.delete(sala)
    db.commit()
    return {"detail": "Sala deletada com sucesso"}
