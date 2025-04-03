from fastapi import HTTPException
from pydantic import BaseModel, field_validator
class UserCreate(BaseModel):
    name: str
    email: str

    @field_validator("email")
    @classmethod  # Adicione o decorador @classmethod
    def validate_email(cls, value):
        try:
            # Verifica se o e-mail contém um "@"
            if "@" not in value:
                raise ValueError("E-mail inválido")
            return value
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True