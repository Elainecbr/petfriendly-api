"""
Schemas Pydantic para o módulo de usuários.
"""

from pydantic import BaseModel, ConfigDict


class EasyLoginRequest(BaseModel):
    """
    Dados recebidos do front-end no Easy Login.
    """

    name: str
    cpf: str
    phone: str


class UserResponse(BaseModel):
    """
    Dados retornados pela API após criação/atualização do usuário.
    """

    id: int
    name: str
    cpf: str
    phone: str

    model_config = ConfigDict(from_attributes=True)