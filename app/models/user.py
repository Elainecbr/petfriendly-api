"""
Model ORM da tabela de usuários.

No MVP, esta tabela é usada pelo Easy Login, permitindo associar
favoritos ao usuário que realizou o login.
"""

from sqlalchemy import Column, Integer, String

from app.database.database import Base


class User(Base):
    """
    Representa um usuário identificado pelo Easy Login.

    O CPF funciona como identificador único do usuário neste MVP.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=False)