# app/schemas/__init__.py
from .user import UserCreate, User  # Exporta os esquemas

__all__ = ["UserCreate", "User"]  # Define o que será importado com `from app.schemas import *`