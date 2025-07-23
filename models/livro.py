from pydantic import BaseModel, Field
from typing import Optional

class LivroBase(BaseModel):
    titulo: str = Field(min_length=3, max_length=50)  # Título deve ter entre 3 e 50 caracteres
    autor: str = Field(min_length=3)
    ano: Optional[int] = Field(None, gt=1000)  # O ano, se fornecido, deve ser maior que 1000

# Modelo para criação de livros (sem ID)
class LivroCreate(LivroBase):
    pass

# Modelo completo do livro (com ID para resposta)
class Livro(LivroBase):
    id: int  # ID sempre presente nas respostas