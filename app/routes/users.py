"""
Rotas do módulo de usuários.

Neste MVP, o login é simplificado:
- o usuário informa nome, CPF e telefone;
- se o CPF já existir, os dados são atualizados;
- se não existir, o usuário é criado.

Esse fluxo permite associar favoritos a um usuário sem implementar
autenticação completa com senha e token.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user_schema import EasyLoginRequest, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/easy-login", response_model=UserResponse)
def easy_login(payload: EasyLoginRequest, db: Session = Depends(get_db)):
    """
    Cria ou atualiza um usuário com base no CPF informado.

    Regras:
    - CPF deve ter 11 dígitos;
    - CPF funciona como identificador único do usuário.
    """
    cpf = payload.cpf.strip()
    cpf_digits = cpf.replace(".", "").replace("-", "")

    if len(cpf_digits) != 11:
        raise HTTPException(status_code=400, detail="CPF inválido")

    user = db.query(User).filter(User.cpf == cpf).first()

    if user:
        user.name = payload.name.strip()
        user.phone = payload.phone.strip()
    else:
        user = User(
            name=payload.name.strip(),
            cpf=cpf,
            phone=payload.phone.strip(),
        )
        db.add(user)

    db.commit()
    db.refresh(user)
    return user