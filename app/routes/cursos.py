from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db

router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.post("/", response_model=schemas.Curso)
def create_curso(curso_data: schemas.CursoCreate, db: Session = Depends(get_db)):
    """Cria um novo curso"""
    return crud.create_curso(db, curso_data)


@router.get("/", response_model=list[schemas.Curso])
def get_cursos(db: Session = Depends(get_db)):
    """Consulta de todos os cursos no banco de dados."""
    return db.query(models.Cursos).all()


@router.get("/{curso_id}", response_model=schemas.Curso)
def get_curso(curso_id: int, db: Session = Depends(get_db)):
    """Consulta de um curso específico."""
    curso = db.query(models.Cursos).filter(models.Cursos.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso


@router.put("/{curso_id}", response_model=schemas.Curso)
def update_curso(curso_id: int, curso_data: schemas.CursoCreate, db: Session = Depends(get_db)):
    """Altera/atualiza as informações de um curso."""
    curso = db.query(models.Cursos).filter(models.Cursos.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    curso.nome = curso_data.nome

    db.commit()
    db.refresh(curso)
    return curso


@router.delete("/{curso_id}")
def delete_curso(curso_id: int, db: Session = Depends(get_db)):
    """Deleta um curso."""
    curso = db.query(models.Cursos).filter(models.Cursos.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    db.delete(curso)
    db.commit()
    return {"detail": "Curso deletado com sucesso"}
