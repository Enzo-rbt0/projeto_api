from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, User
from app.crud.user import (  # Importa as operações CRUD
    get_user,
    get_users,
    create_user,
    update_user,
    delete_user,
)
from app.database import get_db  # Importa a sessão do banco de dados

# Cria um roteador para os endpoints de usuários
router = APIRouter(prefix="/usuarios", tags=["usuarios"])

# Inserir Usuário
@router.post("/inserir", response_model=User)
def inserir_usuario(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

# Listar Usuários
@router.get("/listar", response_model=list[User])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return get_users(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

# Buscar Usuário por ID
@router.get("/buscar/{user_id}", response_model=User)
def buscar_usuario(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = get_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

# Atualizar Usuário
@router.put("/atualizar/{user_id}", response_model=User)
def atualizar_usuario(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = update_user(db, user_id, user)
        if db_user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

# Excluir Usuário
@router.delete("/excluir/{user_id}", response_model=User)
def excluir_usuario(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = delete_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")