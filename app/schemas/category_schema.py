"""
Schemas Pydantic para categorias.

Usados para validar e serializar a saída da API.
"""

from pydantic import BaseModel, ConfigDict


class CategoryResponse(BaseModel):
    """
    Schema de resposta para listagem de categorias.
    """

    id: int
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)