from fastapi import FastAPI
from app.routes import blocos, salas, coordenadores, cursos, reservas

app = FastAPI(
    title="Sistema de Reservas de Salas",
    description="API para gerenciamento de blocos, salas e reservas.",
    version="1.0"
)


app.include_router(cursos.router)
app.include_router(coordenadores.router)
app.include_router(blocos.router)
app.include_router(salas.router)
app.include_router(reservas.router)
