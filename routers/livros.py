from fastapi import HTTPException, APIRouter, Depends
from typing import List
from models.livro import Livro, LivroCreate
from database import get_db_connection
import psycopg2

router = APIRouter() # Organiza as rotas relacionadas a livros

# Rota para obter todos os livros
@router.get("/livros", response_model=List[Livro])
def obter_livros(db=Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM livros")
        livros = cursor.fetchall()
        cursor.close()
        return [Livro(id=l[0], titulo=l[1], autor=l[2], ano=l[3]) for l in livros]
    except (Exception, psycopg2.Error) as error:
        print("Erro ao buscar livros:", error)
        raise HTTPException(status_code=500, detail="Erro ao buscar livros do banco de dados")

# Rota para adicionar um novo livro
@router.post("/livros", response_model=Livro, status_code=201)
def adicionar_livro(livro: LivroCreate, db=Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        # Não incluímos o ID no INSERT, ele será gerado automaticamente
        query = "INSERT INTO livros (titulo, autor, ano) VALUES (%s, %s, %s) RETURNING id"
        cursor.execute(query, (livro.titulo, livro.autor, livro.ano))
        
        # Pega o ID gerado automaticamente
        novo_id = cursor.fetchone()[0]
        
        db.commit()
        cursor.close()
        
        # Retorna o livro completo com o ID gerado
        return Livro(id=novo_id, titulo=livro.titulo, autor=livro.autor, ano=livro.ano)
    except (Exception, psycopg2.Error) as error:
        db.rollback()
        print("Erro ao adicionar livro:", error)
        raise HTTPException(status_code=500, detail="Erro ao adicionar livro no banco de dados")