# app/models/__init__.py
from .user import User  # Exporta o modelo User

__all__ = ["User"]  # Define o que será importado com `from app.models import *`