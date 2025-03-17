from fastapi import FastAPI
from app.api.endpoints import user  # Importa o roteador de usuários
from app.database import engine, Base  # Importa a configuração do banco de dados

"""
# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)
"""

# Cria a aplicação FastAPI
app = FastAPI()

# Inclui o roteador de usuários
app.include_router(user.router)