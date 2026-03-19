"""
Model ORM da tabela de categorias.

As categorias são usadas no front-end como base de filtro visual
para organizar os tipos de locais pet friendly.
"""

from sqlalchemy import Column, Integer, String

from app.database.database import Base


class Category(Base):
    """
    Representa uma categoria cadastrada no banco.

    Campos:
    - id: identificador interno;
    - name: nome exibido ao usuário;
    - slug: nome técnico usado em filtros e integrações.
    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True)
    slug = Column(String(80), nullable=False, unique=True)