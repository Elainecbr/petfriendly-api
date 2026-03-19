"""
Model ORM da tabela de favoritos.

Cada registro representa um local salvo por um usuário.
"""

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from app.database.database import Base


class Place(Base):
    """
    Representa um local favorito salvo pelo usuário.

    user_id:
        faz a ligação entre o favorito e o usuário dono desse registro.
    """

    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    name = Column(String(120), nullable=False)
    category = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    distance_km = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)