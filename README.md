# Sistema de Reservas de Salas Acadêmicas

## Descrição

Essa API, desenvolvida em Python com o framework FastAPI, foi criada para compor um sistema que a UniEVANGÉLICA usará 
para o gerenciamento de reservas de salas acadêmicas. Suas funcionalidades-chave incluem:
- **Cadastro de Blocos e Salas**  
  - Cadastro de blocos com nome e associação a um curso.
  - Cadastro de salas associadas a um bloco, com atributos como número, capacidade, recursos e indicação se a sala é exclusiva para um curso.  
  - Ao criar uma sala, o `curso_id` é herdado automaticamente do bloco relacionado.

- **Gerenciamento de Reservas**  
  - Permite que coordenadores reservem salas em horários específicos.
  - Validação para evitar reservas duplicadas ou sobrepostas.
  - Regras de negócio para que, se uma sala for exclusiva, apenas coordenadores vinculados ao curso possam reservar.

- **Cadastro de Coordenadores e Cursos**  
  - Cadastro e gerenciamento de coordenadores, vinculando-os a um curso.
  - Cadastro e atualização de cursos.

---

## Tecnologias Utilizadas

- **Python 3.x**
- **FastAPI**: Framework para a criação de APIs REST de alta performance.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **PostgreSQL**: Banco de dados relacional.
- **Uvicorn**: Servidor ASGI para rodar a aplicação.
- **Pydantic**: Validação e definição dos modelos de dados.
- **Passlib**: Para hashing seguro de senhas.

---

## Instalação

### Pré-requisitos

- Python 3.x instalado.
- PostgreSQL instalado e rodando.
- Executar `pip install bcrypt passlib` no terminal.



### Passo a passo

1. **Clonar o Repositório**
    ```bash
   git clone https://github.com/EduardoHansel/teste.git
   cd teste
   
2. **Criar e Ativar o Ambiente Virtual (recomendado)**
    ```bash
   python -m venv .venv
   .venv\Scripts\activate

3. **Instalar as Dependências**
    ```bash
    pip install -r requirements.txt
   ```
   Certifique-se de que todos os módulos e pacotes estão instalados.
   
4. **Configurar o Banco de Dados**
- Dentro do `PostgreSQL / pgAdmin 4`, crie um banco de dados (Default Workspace > Databases (botão direito) > Create > Database...).
- Em `database.py`, ajuste a quinta linha do código com sua senha do PostgreSQL e o nome do banco de dados:
  - ```URL_DATABASE = "postgresql://postgres:SUASENHA@localhost:5432/NOMEDOSEUBANCO"```
- Após a criar o banco de dados, execute o código a seguir para criar as tabelas (selecione o banco de dados criado (botão direito) > Query tool > colar o código e executar).

```
-- Criação da tabela cursos (deve vir primeiro)
CREATE TABLE cursos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Criação da tabela blocos
CREATE TABLE blocos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    curso_id INTEGER NOT NULL,
    CONSTRAINT fk_blocos_cursos FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

-- Criação da tabela salas
CREATE TABLE salas (
    id SERIAL PRIMARY KEY,
    bloco_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    numero INTEGER NOT NULL CHECK (numero > 0),
    capacidade INTEGER NOT NULL CHECK (capacidade > 0),
    recursos VARCHAR(100) NOT NULL,
    exclusivo BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_salas_blocos FOREIGN KEY (bloco_id) REFERENCES blocos(id) ON DELETE CASCADE,
    CONSTRAINT fk_salas_cursos FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

-- Criação da tabela coordenadores
CREATE TABLE coordenadores (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    CONSTRAINT fk_coordenadores_cursos FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

-- Criação da tabela reservas
CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    sala_id INTEGER NOT NULL,
    coordenador_id INTEGER NOT NULL,
    data_reserva DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    motivo VARCHAR(100) NOT NULL,
    CONSTRAINT fk_reservas_salas FOREIGN KEY (sala_id) REFERENCES salas(id) ON DELETE CASCADE,
    CONSTRAINT fk_reservas_coordenadores FOREIGN KEY (coordenador_id) REFERENCES coordenadores(id) ON DELETE CASCADE
);
```

---

## Execução

Para iniciar a API, execute o seguinte comando no terminal:

`uvicorn app.main:app --reload`

A API estará disponível em:

`http://127.0.0.1:8000/`

### Documentação Interativa

O FastAPI gera automaticamente uma documentação interativa, acessível em:

- Swagger UI: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

---

## Endpoints

- ### Blocos

    - `POST /blocos/` – Criação de bloco (inclui nome e curso_id).
    
    - `GET /blocos/` – Listagem de todos os blocos.
    
    - `GET /blocos/{id}` – Consulta de bloco específico.
    
    - `PUT /blocos/{id}` – Atualização de bloco.
    
    - `DELETE /blocos/{id}` – Exclusão de bloco (e suas salas associadas).

- ### Salas

    - `POST /salas/` – Criação de sala (o curso_id é herdado do bloco).
    
    - `GET /salas/` – Listagem de salas.
    
    - `GET /salas/{id}` – Consulta de sala específica.
    
    - `PUT /salas/{id}` – Atualização de sala.
    
    - `DELETE /salas/{id}` – Exclusão de sala.

- ### Reservas

    - `POST /reservas/` – Criação de reserva (com verificação de conflito de horários e regras para reservas exclusivas).
    
    - `GET /reservas/` – Listagem de reservas.
    
    - `GET /reservas/{id}` – Consulta de reserva específica.
    - `GET /reservas/proxima_semana` - Consulta das reservas para os próximos 7 dias.
    
    - `PUT /reservas/{id}` – Atualização de reserva.
    
    - `DELETE /reservas/{id}` – Exclusão de reserva.

- ### Coordenadores

    - `POST /coordenadores/` – Criação de coordenador.
    
    - `GET /coordenadores/` – Listagem de coordenadores.
    
    - `GET /coordenadores/{id}` – Consulta de coordenador específico.
    
    - `PUT /coordenadores/{id}` – Atualização de coordenador.
    
    - `DELETE /coordenadores/{id}` – Exclusão de coordenador.

- ### Cursos

    - `POST /cursos/` – Criação de curso.
    
    - `GET /cursos/` – Listagem de cursos.
    
    - `GET /cursos/{id}` – Consulta de curso específico.
    
    - `PUT /cursos/{id}` – Atualização de curso.
    
    - `DELETE /cursos/{id}` – Exclusão de curso.
