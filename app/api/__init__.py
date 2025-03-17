# app/api/__init__.py
from .endpoints import user  # Exporta o roteador de usuários

__all__ = ["user"]  # Define o que será importado com `from app.api import *`