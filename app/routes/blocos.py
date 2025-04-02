from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db

router = APIRouter(prefix="/blocos", tags=["Blocos"])

@router.post("/", response_model=schemas.Bloco)
def create_bloco(bloco_data: schemas.BlocoCreate, db: Session = Depends(get_db)):
    """Cria um novo bloco relacionado a um curso"""
    return crud.create_bloco(db, bloco_data)

@router.get("/", response_model=list[schemas.Bloco])
def get_blocos(db: Session = Depends(get_db)):
    """Consulta de todos os blocos no banco de dados."""
    return db.query(models.Blocos).all()

@router.get("/{bloco_id}", response_model=schemas.Bloco)
def get_bloco(bloco_id: int, db: Session = Depends(get_db)):
    """Consulta de um bloco específico."""
    bloco = db.query(models.Blocos).filter(models.Blocos.id == bloco_id).first()
    if not bloco:
        raise HTTPException(status_code=404, detail="Bloco não encontrado")
    return bloco

@router.put("/{bloco_id}", response_model=schemas.Bloco)
def update_bloco(bloco_id: int, bloco_data: schemas.BlocoCreate, db: Session = Depends(get_db)):
    """Altera/atualiza as informações de um bloco."""
    bloco = db.query(models.Blocos).filter(models.Blocos.id == bloco_id).first()
    if not bloco:
        raise HTTPException(status_code=404, detail="Bloco não encontrado")
    bloco.nome = bloco_data.nome
    bloco.curso_id = bloco_data.curso_id
    db.commit()
    db.refresh(bloco)
    return bloco

@router.delete("/{bloco_id}")
def delete_bloco(bloco_id: int, db: Session = Depends(get_db)):
    """Deleta o bloco e suas salas relacionadas."""
    bloco = db.query(models.Blocos).filter(models.Blocos.id == bloco_id).first()
    if not bloco:
        raise HTTPException(status_code=404, detail="Bloco não encontrado")

    db.query(models.Salas).filter(models.Salas.bloco_id == bloco_id).delete()

    db.delete(bloco)
    db.commit()
