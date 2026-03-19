"""
Seed inicial do banco.

Este módulo garante que categorias básicas existam na aplicação
logo após a criação das tabelas.
"""

from app.database.database import SessionLocal
from app.models.category import Category


def seed_categories():
    """
    Insere as categorias padrão do sistema, caso ainda não existam.

    A função é idempotente: pode ser chamada várias vezes sem duplicar dados.
    """
    db = SessionLocal()

    categorias = [
        {"name": "Parque-Outdoor", "slug": "parque-outdoor"},
        {"name": "Parque-Indoor", "slug": "parque-indoor"},
        {"name": "Hotel-Pousada", "slug": "hotel-pousada"},
        {"name": "Veterinária", "slug": "veterinaria"},
        {"name": "Restaurante-Café", "slug": "restaurante-cafe"},
        {"name": "Todos", "slug": "todos"},
    ]

    for cat in categorias:
        existe = db.query(Category).filter_by(slug=cat["slug"]).first()
        if not existe:
            db.add(Category(**cat))

    db.commit()
    db.close()