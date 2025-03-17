# app/crud/__init__.py
from .user import (  # Exporta as funções CRUD
    get_user,
    get_users,
    create_user,
    update_user,
    delete_user,
)

__all__ = [
    "get_user",
    "get_users",
    "create_user",
    "update_user",
    "delete_user",
]