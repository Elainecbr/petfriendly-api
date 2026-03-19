"""
Configuração central do banco de dados da aplicação.

Responsabilidades deste módulo:
- criar a engine do SQLAlchemy;
- criar a fábrica de sessões;
- expor a classe Base para os models;
- fornecer a dependência get_db() usada nas rotas do FastAPI.

A persistência do MVP acontece em SQLite, por simplicidade de setup
e aderência à especificação da disciplina.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL de conexão do SQLite.
# O arquivo petfriendly.db será criado na raiz do projeto quando necessário.
SQLALCHEMY_DATABASE_URL = "sqlite:///./petfriendly.db"

# Engine principal de conexão com o banco.
# check_same_thread=False é necessário para SQLite em cenários com FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Fábrica de sessões.
# autocommit=False e autoflush=False dão mais controle ao fluxo das transações.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base herdada por todos os models ORM.
Base = declarative_base()


def get_db():
    """
    Dependência usada nas rotas FastAPI.

    Abre uma sessão com o banco para cada requisição e garante o fechamento
    ao final do ciclo, evitando vazamento de conexão.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()