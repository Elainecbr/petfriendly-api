"""
Rotas do módulo de categorias.

Este módulo expõe os filtros disponíveis para a interface.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.category import Category
from app.schemas.category_schema import CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """
    Lista todas as categorias cadastradas no banco.

    A ordenação alfabética facilita a renderização estável no front-end.
    """
    return db.query(Category).order_by(Category.name).all()