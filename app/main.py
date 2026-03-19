"""
Ponto de entrada da aplicação FastAPI.

Este módulo:
- cria a instância principal do app;
- registra CORS;
- cria as tabelas do banco;
- executa seed inicial;
- registra as rotas.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.database.seed import seed_categories
from app.models.category import Category  # noqa: F401
from app.models.place import Place  # noqa: F401
from app.models.user import User  # noqa: F401
from app.routes.categories import router as categories_router
from app.routes.places import router as places_router
from app.routes.users import router as users_router
from app.routes.weather import router as weather_router

app = FastAPI(
    title="PetFriendly API",
    version="1.0.0",
    description="API para busca de lugares pet friendly, cálculo de rota, clima e favoritos por usuário.",
)

# CORS liberado para facilitar integração com o front-end local.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas caso ainda não existam.
Base.metadata.create_all(bind=engine)

# Insere categorias padrão.
seed_categories()

# Registro dos módulos de rota.
app.include_router(places_router)
app.include_router(categories_router)
app.include_router(weather_router)
app.include_router(users_router)


@app.get("/health", tags=["Health"])
def health():
    """
    Endpoint simples para verificar se a API está no ar.
    """
    return {"status": "ok"}