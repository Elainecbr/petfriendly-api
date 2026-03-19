"""
Serviços de integração com a API do Google.

Este módulo centraliza:
- busca textual de locais pet friendly;
- cálculo de rota entre origem e destino.

A separação em 'services' ajuda a manter as rotas enxutas
e com responsabilidade única.
"""

import requests
from requests import RequestException

from app.config.settings import settings

GOOGLE_PLACES_TEXTSEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
GOOGLE_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"


def _ensure_google_api_key() -> None:
    """
    Garante que a chave da API do Google esteja configurada.

    Sem essa validação, a aplicação tentaria fazer chamadas inválidas.
    """
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY não configurada no .env")


def _validate_google_status(payload: dict, context: str) -> None:
    """
    Valida o status devolvido pelo Google.

    Alguns retornos são considerados válidos mesmo sem resultados.
    """
    status = payload.get("status")
    if status in {"OK", "ZERO_RESULTS"}:
        return

    error_message = payload.get("error_message", "sem detalhes")
    raise ValueError(f"{context} falhou: status={status} | detalhe={error_message}")


def search_pet_friendly_places(
    location: str,
    keyword: str = "pet friendly",
    radius: int = 3000,
) -> dict:
    """
    Busca locais pet friendly no Google Places.

    Args:
        location: texto livre com bairro, cidade ou endereço.
        keyword: termo complementar de busca.
        radius: raio aproximado da busca em metros.

    Returns:
        JSON bruto da API do Google Places.
    """
    _ensure_google_api_key()

    params = {
        "query": f"{keyword} em {location}",
        "radius": radius,
        "language": "pt-BR",
        "region": "br",
        "key": settings.google_api_key,
    }

    try:
        response = requests.get(
            GOOGLE_PLACES_TEXTSEARCH_URL,
            params=params,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        _validate_google_status(data, "Busca de locais")
        return data
    except RequestException as exc:
        raise RuntimeError(f"Falha de comunicação com Google Places: {exc}") from exc


def get_route(origin: str, destination: str, mode: str = "walking") -> dict:
    """
    Calcula rota no Google Directions.

    Args:
        origin: ponto de partida.
        destination: destino desejado.
        mode: modo de transporte (walking, driving, bicycling, transit).

    Returns:
        JSON bruto da API do Google Directions.
    """
    _ensure_google_api_key()

    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "language": "pt-BR",
        "region": "br",
        "key": settings.google_api_key,
    }

    try:
        response = requests.get(
            GOOGLE_DIRECTIONS_URL,
            params=params,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        _validate_google_status(data, "Cálculo de rota")
        return data
    except RequestException as exc:
        raise RuntimeError(f"Falha de comunicação com Google Directions: {exc}") from exc