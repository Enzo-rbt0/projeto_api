from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body
from sqlalchemy.orm import Session
from app.services.pdf import generate_user_pdf
from app.services.email import send_email
import os
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
    
@router.post("/get_pdf_user")
async def get_pdf_user(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        # 1. Pega seu e-mail do .env
        recipient = os.getenv("DEFAULT_RECIPIENT")
        if not recipient:
            raise HTTPException(
                status_code=400,
                detail="Configure DEFAULT_RECIPIENT no arquivo .env"
            )

        # 2. Busca usuários
        users = get_users(db, skip=0, limit=100)
        if not users:
            raise HTTPException(
                status_code=404,
                detail="Nenhum usuário cadastrado"
            )

        # 3. Gera PDF
        pdf_path = generate_user_pdf(users)
        
        # 4. Envia por e-mail (em background)
        background_tasks.add_task(
            send_email,
            to_email=recipient,  # Seu e-mail fixo
            subject="Relatório de Usuários",
            body="Segue em anexo o relatório completo.",
            filename=pdf_path
        )
        
        return {
            "message": f"Relatório enviado para {recipient}",
            "users_count": len(users)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar: {str(e)}"
        )

@router.post("/email_to")
async def send_pdf_to_email(
    email: str = Body(..., embed=True, description="E-mail do destinatário"),  # E-mail obrigatório
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    try:
        # Validação básica do e-mail
        if "@" not in email or "." not in email.split("@")[-1]:
            raise HTTPException(
                status_code=400,
                detail="Formato de e-mail inválido. Use: usuario@provedor.com"
            )

        # Busca usuários
        users = get_users(db, skip=0, limit=100)
        if not users:
            raise HTTPException(
                status_code=404,
                detail="Nenhum usuário cadastrado no banco de dados"
            )

        # Gera PDF
        pdf_path = generate_user_pdf(users)
        
        # Envia e-mail em segundo plano
        background_tasks.add_task(
            send_email,
            to_email=email,
            subject="Relatório de Usuários (Enviado por você)",
            body=f"Segue em anexo o relatório completo com {len(users)} usuários cadastrados.",
            filename=pdf_path
        )
        
        return {
            "message": f"PDF será enviado para {email}",
            "users_count": len(users)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Falha ao processar: {str(e)}"
        )