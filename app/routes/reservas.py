from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from datetime import date, time

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.post("/", response_model=schemas.Reserva)
def create_reserva(reserva_data: schemas.ReservaCreate, db: Session = Depends(get_db)):
    """Cria uma nova reserva"""
    return crud.create_reserva(db, reserva_data)


@router.get("/", response_model=list[schemas.Reserva])
def get_reservas(db: Session = Depends(get_db)):
    """Consulta de todos as reservas no banco de dados."""
    return db.query(models.Reservas).all()


@router.get("/{reserva_id}", response_model=schemas.Reserva)
def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Consulta de uma reserva específica."""
    reserva = db.query(models.Reservas).filter(models.Reservas.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva


@router.put("/{reserva_id}", response_model=schemas.Reserva)
def update_reserva(reserva_id: int, reserva_data: schemas.ReservaCreate, db: Session = Depends(get_db)):
    """Altera/atualiza as informações de uma reserva."""
    reserva = db.query(models.Reservas).filter(models.Reservas.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    reserva.sala_id = reserva_data.sala_id
    reserva.coordenador_id = reserva_data.coordenador_id
    reserva.data_reserva = reserva_data.data_reserva
    reserva.hora_inicio = reserva_data.hora_inicio
    reserva.hora_fim = reserva_data.hora_fim
    reserva.motivo = reserva_data.motivo
    db.commit()
    db.refresh(reserva)
    return reserva


@router.delete("/{reserva_id}")
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Cancela uma reserva uma reserva."""
    reserva = db.query(models.Reservas).filter(models.Reservas.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    db.delete(reserva)
    db.commit()
    return {"detail": "Reserva cancelada com sucesso"}

@router.get("/disponibilidade/")
def verificar_disponibilidade(sala_id: int, data: date, hora_inicio: time, hora_fim: time, db: Session = Depends(get_db)):
    """Verifica se uma sala está disponível em um determinado horário. (data: aaaa-mm-dd | hora: hh:mm:ss)"""
    reserva_existente = db.query(models.Reservas).filter(
        models.Reservas.sala_id == sala_id,
        models.Reservas.data_reserva == data,
        models.Reservas.hora_inicio < hora_fim,
        models.Reservas.hora_fim > hora_inicio
    ).first()

    if reserva_existente:
        return {"disponivel": False, "mensagem": "A sala já está reservada nesse horário."}
    return {"disponivel": True, "mensagem": "A sala está disponível para reserva."}
