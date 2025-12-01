#database/db.py
import sqlite3
import os

# ----------------------------------------------------------------------
# CORREÇÃO PARA APONTAR PARA A RAIZ DO PROJETO (Praticidade!)
# ----------------------------------------------------------------------
# os.path.dirname(__file__) = 'SFA-Sistema_Familias_Assistidas/database'
# os.path.dirname(...) de novo leva para: 'SFA-Sistema_Familias_Assistidas/' (A Raiz)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(base_dir, "familias.db")
# ----------------------------------------------------------------------

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_connection():
    """Abre conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_NAME) 
    return conn

def migrar_db():
    """
    Função de Migração: Cria a tabela 'usuarios' se ela ainda não existir
    no banco de dados existente.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    sql_usuarios = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        funcao TEXT NOT NULL 
    );
    """
    
    try:
        print("🔧 Verificando e adicionando tabelas faltantes...")
        cursor.executescript(sql_usuarios)
        conn.commit()
        print("✅ Tabela 'usuarios' verificada/criada com sucesso!")
        return True
    
    except Exception as e:
        print(f"❌ Erro ao migrar banco: {e}")
        return False
    finally:
        conn.close()

def init_db():
    """Cria o banco de dados a partir do schema.sql, caso não exista."""
    if not os.path.exists(DB_NAME):
        print("📦 Criando banco de dados...")
        conn = get_connection()
        cursor = conn.cursor()

        try:
            with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
                schema = f.read()
                cursor.executescript(schema)
            conn.commit()
            print("✅ Banco de dados criado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao criar o banco: {e}")
        finally:
            conn.close()
    else:
        print("✔ Banco já existente.")


if __name__ == "__main__":
    # Garante que o banco base (se não existir) seja criado
    init_db()
    # Adiciona a tabela 'usuarios' ao banco existente sem perder dados
    migrar_db()