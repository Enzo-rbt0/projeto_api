# app/api/endpoints/__init__.py
from .user import router as user_router  # Exporta o roteador de usuários

__all__ = ["user_router"]  # Define o que será importado com `from app.api.endpoints import *`