from fastapi import FastAPI, Response, status
from routers import livros
from database import create_livros_table
from contextlib import asynccontextmanager

# Função para gerenciar o ciclo de vida da aplicação
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: executa quando a aplicação inicia

    print("Iniciando aplicação...")
    create_livros_table()
    yield # yield permite que a aplicação continue rodando
    
    # Shutdown: executa quando a aplicação é encerrada
    print("Encerrando aplicação...")

app = FastAPI(lifespan=lifespan) # Define a API de forma completa

@app.get("/")
def ler_raiz():
    return {"Olá": "Bem-vindo à API de Livros!"}

@app.api_route("/health", methods=["GET", "HEAD"], status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok", "message": "Backend is alive!"}

app.include_router(livros.router)