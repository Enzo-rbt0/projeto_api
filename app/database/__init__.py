# app/database/__init__.py
from .session import engine, Base, get_db  # Exporta a configuração do banco de dados

__all__ = ["engine", "Base", "get_db"]  # Define o que será importado com `from app.database import *`