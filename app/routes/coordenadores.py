from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db

router = APIRouter(prefix="/coordenadores", tags=["Coordenadores"])

@router.post("/", response_model=schemas.Coordenador)
def create_coordenador(coordenador_data: schemas.CoordenadorCreate, db: Session = Depends(get_db)):
    """Cria um novo coordenador"""
    return crud.create_coordenador(db, coordenador_data)


@router.get("/", response_model=list[schemas.Coordenador])
def get_coordenadores(db: Session = Depends(get_db)):
    """Consulta de todos os coordenadores no banco de dados."""
    return db.query(models.Coordenadores).all()


@router.get("/{coordenador_id}", response_model=schemas.Coordenador)
def get_coordenador(coordenador_id: int, db: Session = Depends(get_db)):
    """Consulta de um coordenador específico."""
    coordenador = db.query(models.Coordenadores).filter(models.Coordenadores.id == coordenador_id).first()
    if not coordenador:
        raise HTTPException(status_code=404, detail="Coordenador não encontrado")
    return coordenador


@router.put("/{coordenador_id}", response_model=schemas.Coordenador)
def update_coordenador(coordenador_id: int, coordenador_data: schemas.CoordenadorCreate, db: Session = Depends(get_db)):
    """Altera/atualiza as informações de um coordenador."""
    coordenador = db.query(models.Coordenadores).filter(models.Coordenadores.id == coordenador_id).first()
    if not coordenador:
        raise HTTPException(status_code=404, detail="Coordenador não encontrado")

    coordenador.curso_id = coordenador_data.curso_id
    coordenador.nome = coordenador_data.nome
    coordenador.email = coordenador_data.email
    coordenador.senha = crud.hash_senha(coordenador_data.senha)

    db.commit()
    db.refresh(coordenador)
    return coordenador


@router.delete("/{coordenador_id}")
def delete_coordenador(coordenador_id: int, db: Session = Depends(get_db)):
    """Deleta um coordenador."""
    coordenador = db.query(models.Coordenadores).filter(models.Coordenadores.id == coordenador_id).first()
    if not coordenador:
        raise HTTPException(status_code=404, detail="Coordenador não encontrado")
    db.delete(coordenador)
    db.commit()
    return {"detail": "Coordenador deletado com sucesso"}
