import dotenv
import os
import psycopg2 # Importa a biblioteca psycopg2 para conexão com PostgreSQL

from psycopg2 import Error
from fastapi import HTTPException

def get_db_connection():
    # Carrega as variáveis de ambiente do arquivo .env
    dotenv.load_dotenv()
    
    connection = None
    
    try:
        # Conecta ao banco de dados usando as variáveis de ambiente
        connection = psycopg2.connect(
            host=os.getenv('PGHOST'),
            database=os.getenv('PGDATABASE'),
            user=os.getenv('PGUSER'),
            password=os.getenv('PGPASSWORD'),
            port=os.getenv('PGPORT'),
            sslmode=os.getenv('PGSSLMODE'),
            channel_binding=os.getenv('PGCHANNELBINDING')
        )
        print("Conexão com o banco de dados estabelecida com sucesso.")
        yield connection # Isto permite que a conexão seja usada como um gerador, fechando-a automaticamente após o uso.
        
    except (Exception, Error) as error:
        print("Erro ao conectar ao banco de dados:", error)
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados")
    
    finally:
        if connection:
            connection.close()
            print("Conexão com o banco de dados fechada.")

def create_livros_table():
    """Cria a tabela 'livros' no banco de dados se ela não existir."""
    try:
        # Usa o gerador de conexão do database.py
        connection_generator = get_db_connection()
        connection = next(connection_generator)
        
        cursor = connection.cursor()
        
        # A cláusula "IF NOT EXISTS" previne erros se a tabela já existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id SERIAL PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                autor VARCHAR(255) NOT NULL,
                ano INT NOT NULL
            );
        """)
        
        connection.commit()
        cursor.close()
        print("Tabela 'livros' verificada/criada com sucesso.")

        # Fecha a conexão manualmente já que não estamos usando o gerador completo
        connection.close()
        
    except (Exception, Error) as error:
        print("Erro ao criar a tabela:", error)