"""
Schemas Pydantic para favoritos.

Separam claramente:
- criação;
- atualização parcial;
- resposta da API.
"""

from pydantic import BaseModel, ConfigDict


class PlaceBase(BaseModel):
    """
    Campos comuns de um local favorito.
    """

    name: str
    category: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    distance_km: float | None = None
    rating: float | None = None


class PlaceCreate(PlaceBase):
    """
    Schema usado para criar um favorito.

    O user_id não vem no body: ele é enviado como query param e
    injetado na rota para associar o favorito ao usuário.
    """


class PlaceUpdate(BaseModel):
    """
    Schema usado para atualização parcial de favorito.
    """

    name: str | None = None
    category: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    distance_km: float | None = None
    rating: float | None = None


class PlaceResponse(PlaceBase):
    """
    Schema de resposta para um favorito salvo no banco.
    """

    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
