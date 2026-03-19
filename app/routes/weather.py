"""
Rotas de clima.

Este módulo consulta a API OpenWeather e devolve apenas os campos
relevantes para o dashboard.
"""

import requests
from fastapi import APIRouter, HTTPException

from app.config.settings import settings

router = APIRouter(prefix="/weather", tags=["Weather"])

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@router.get("/")
def get_weather(city: str):
    """
    Retorna clima atual de uma cidade.

    A resposta é simplificada para reduzir acoplamento com o front-end.
    """
    if not settings.openweather_api_key:
        raise HTTPException(
            status_code=400,
            detail="OPENWEATHER_API_KEY não configurada no .env",
        )

    try:
        res = requests.get(
            WEATHER_URL,
            params={
                "q": city,
                "appid": settings.openweather_api_key,
                "units": "metric",
                "lang": "pt_br",
            },
            timeout=10,
        )
        res.raise_for_status()
        data = res.json()

        return {
            "cidade": data["name"],
            "temperatura": data["main"]["temp"],
            "sensacao": data["main"]["feels_like"],
            "humidade": data["main"]["humidity"],
            "descricao": data["weather"][0]["description"],
            "icone": f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar clima: {exc}")