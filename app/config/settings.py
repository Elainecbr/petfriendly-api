"""
Leitura centralizada de variáveis de ambiente.

Este módulo concentra chaves e configurações externas da aplicação,
evitando espalhar segredos e parâmetros sensíveis pelo código.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Caminho base do projeto petfriendly-api.
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Configurações carregadas do arquivo .env.

    google_api_key:
        usada para Google Places e Google Directions.

    openweather_api_key:
        usada para consultar o clima atual.
    """

    google_api_key: str = ""
    openweather_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
    )


# Instância única reutilizada por toda a aplicação.
settings = Settings()