from sqlalchemy import Column, ForeignKey, Integer, String, Time, Date, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Blocos(Base):
    __tablename__ = "blocos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)

    curso = relationship("Cursos", back_populates="blocos")
    salas = relationship("Salas", back_populates="bloco")

class Salas(Base):
    __tablename__ = "salas"

    id = Column(Integer, primary_key=True)
    bloco_id = Column(Integer, ForeignKey("blocos.id"), nullable=False, index=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False, index=True)
    numero = Column(Integer, nullable=False)
    capacidade = Column(Integer, nullable=False)
    recursos = Column(String(100), nullable=False)
    exclusivo = Column(Boolean, nullable=False, default=False)


    bloco = relationship("Blocos", back_populates="salas")
    curso = relationship("Cursos", back_populates="salas")
    reservas = relationship("Reservas", back_populates="sala")

    __table_args__ = (CheckConstraint('capacidade > 0', name='check_capacidade_positiva'),
                      CheckConstraint('numero > 0', name='check_numero_positivo'))


class Coordenadores(Base):
    __tablename__ = "coordenadores"

    id = Column(Integer, primary_key=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)

    reservas = relationship("Reservas", back_populates="coordenador")

class Reservas(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True)
    sala_id = Column(Integer, ForeignKey("salas.id"), nullable=False, index=True)
    coordenador_id = Column(Integer, ForeignKey("coordenadores.id"), nullable=False, index=True)
    data_reserva = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    motivo = Column(String(100), nullable=False)

    sala = relationship("Salas", back_populates="reservas")
    coordenador = relationship("Coordenadores", back_populates="reservas")

class Cursos(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)

    blocos = relationship("Blocos", back_populates="curso")
    salas = relationship("Salas", back_populates="curso")
