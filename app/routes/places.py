"""
Rotas do módulo principal de locais.

Este módulo concentra:
- busca de locais pet friendly;
- cálculo de rota;
- CRUD de favoritos por usuário.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.place import Place
from app.schemas.place_schema import PlaceCreate, PlaceResponse, PlaceUpdate
from app.services.google_places import get_route, search_pet_friendly_places

router = APIRouter(prefix="/places", tags=["Places"])


@router.get("/search")
def search_places(
    location: str = Query(..., min_length=3),
    keyword: str = Query("pet friendly"),
    radius: int = Query(3000, ge=500, le=50000),
):
    """
    Busca locais pet friendly a partir de texto livre.

    Exemplo de uso:
    - bairro;
    - cidade;
    - endereço;
    - CEP convertido previamente no front-end.
    """
    try:
        return search_pet_friendly_places(
            location=location,
            keyword=keyword,
            radius=radius,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/route")
def route_places(
    origin: str = Query(..., min_length=3),
    destination: str = Query(..., min_length=3),
    mode: str = Query("walking", pattern="^(driving|walking|bicycling|transit)$"),
):
    """
    Calcula a rota entre origem e destino.

    O resultado é repassado ao front-end, que exibe distância e duração.
    """
    try:
        return get_route(origin=origin, destination=destination, mode=mode)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.post("/favorites", response_model=PlaceResponse, status_code=201)
def create_favorite(
    payload: PlaceCreate,
    user_id: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    """
    Salva um favorito para um usuário específico.

    O vínculo é feito por meio do parâmetro user_id.
    """
    item = Place(user_id=user_id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/favorites", response_model=list[PlaceResponse])
def list_favorites(
    user_id: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    """
    Lista apenas os favoritos do usuário informado.
    """
    return (
        db.query(Place)
        .filter(Place.user_id == user_id)
        .order_by(Place.id.desc())
        .all()
    )


@router.put("/favorites/{place_id}", response_model=PlaceResponse)
def update_favorite(
    place_id: int,
    payload: PlaceUpdate,
    user_id: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    """
    Atualiza um favorito pertencente ao usuário informado.

    Isso impede que um usuário altere dados de outro.
    """
    item = (
        db.query(Place)
        .filter(Place.id == place_id, Place.user_id == user_id)
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")

    data = payload.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/favorites/{place_id}", status_code=204)
def delete_favorite(
    place_id: int,
    user_id: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    """
    Remove um favorito pertencente ao usuário informado.
    """
    item = (
        db.query(Place)
        .filter(Place.id == place_id, Place.user_id == user_id)
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")

    db.delete(item)
    db.commit()
    return None