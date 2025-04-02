from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def commit_and_refresh(db: Session, entity):
    try:
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco de dados: {str(e)}")

def create_bloco(db: Session, bloco_data: schemas.BlocoCreate):
    bloco = models.Blocos(nome=bloco_data.nome, curso_id=bloco_data.curso_id)
    return commit_and_refresh(db=db, entity=bloco)

def create_sala(db: Session, sala_data: schemas.SalaCreate):
    bloco = db.query(models.Blocos).filter(models.Blocos.id == sala_data.bloco_id).first()

    if not bloco:
        raise HTTPException(status_code=404, detail="Bloco não encontrado")

    sala = models.Salas(
        bloco_id=sala_data.bloco_id,
        curso_id=bloco.__dict__['curso_id'],
        numero=sala_data.numero,
        capacidade=sala_data.capacidade,
        recursos=sala_data.recursos,
        exclusivo=sala_data.exclusivo
    )
    return commit_and_refresh(db=db, entity=sala)

def create_coordenador(db: Session, coordenador_data: schemas.CoordenadorCreate):

    email_existente = db.query(models.Coordenadores).filter(models.Coordenadores.email == coordenador_data.email).first()

    if email_existente:
        raise HTTPException(status_code=400, detail="Erro: Email já cadastrado!")

    coordenador = models.Coordenadores(
        curso_id=coordenador_data.curso_id,
        nome=coordenador_data.nome,
        email=coordenador_data.email,
        senha=hash_senha(coordenador_data.senha)
    )
    return commit_and_refresh(db=db, entity=coordenador)

def create_reserva(db: Session, reserva_data: schemas.ReservaCreate):
    sala_a_ser_reservada = db.query(models.Salas).filter(
        models.Salas.id == reserva_data.sala_id
    ).first()

    if not sala_a_ser_reservada:
        raise HTTPException(status_code=404, detail="Erro: Sala não encontrada.")

    if sala_a_ser_reservada.exclusivo:

        coordenador_reservando = db.query(models.Coordenadores).filter(
            models.Coordenadores.id == reserva_data.coordenador_id
        ).first()

        if coordenador_reservando.curso_id != sala_a_ser_reservada.curso_id:
            raise HTTPException(status_code=403, detail="Erro: Coordenador não possui permissão para reservar essa sala/laboratório.")

    reserva_existente = db.query(models.Reservas).filter(
        models.Reservas.sala_id == reserva_data.sala_id,
        models.Reservas.data_reserva == reserva_data.data_reserva,
        models.Reservas.hora_inicio < reserva_data.hora_fim,
        models.Reservas.hora_fim > reserva_data.hora_inicio
    ).first()

    if reserva_existente:
        raise HTTPException(status_code=400, detail="Erro: A sala já está reservada para esse horário!")

    reserva = models.Reservas(
        sala_id=reserva_data.sala_id,
        coordenador_id=reserva_data.coordenador_id,
        data_reserva=reserva_data.data_reserva,
        hora_inicio=reserva_data.hora_inicio,
        hora_fim=reserva_data.hora_fim,
        motivo=reserva_data.motivo
    )
    return commit_and_refresh(db=db, entity=reserva)

def create_curso(db: Session, curso_data: schemas.CursoCreate):
    curso = models.Cursos(nome=curso_data.nome)
    return commit_and_refresh(db=db, entity=curso)

