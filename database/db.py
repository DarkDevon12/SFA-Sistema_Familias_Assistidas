import sqlite3
import os

DB_NAME = "familias.db"
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_connection():
    """Abre conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_NAME)
    return conn

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
            conn.commit()  # salva todas as alterações
            print("✅ Banco de dados criado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao criar o banco: {e}")
        finally:
            conn.close()  # fecha a conexão, sempre
    else:
        print("✔ Banco já existente.")

if __name__ == "__main__":
    # Roda a inicialização se chamar o arquivo diretamente
    init_db()
