import sqlite3
import hashlib
from database.db import get_connection

def hash_senha(senha):
    """Cria um hash SHA-256 para a senha."""
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def criar_novo_usuario(nome, email, senha):
    """Salva um novo usuário no banco de dados com a senha hasheada."""
    
    senha_hasheada = hash_senha(senha)
    conn = None
    funcao_padrao = "assistente"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = "INSERT INTO usuarios (nome, email, senha, funcao) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (nome, email, senha_hasheada, funcao_padrao))
        
        conn.commit()
        return "Usuário criado com sucesso!"
    
    except sqlite3.IntegrityError:
        return "Erro: Este EMAIL já está em uso."
    except Exception as e:
        return f"Erro inesperado ao salvar: {e}"
    finally:
        if conn:
            conn.close()

# ------------------------------------------------------------------------
# FUNÇÃO ESSENCIAL PARA AUTENTICAÇÃO
# ------------------------------------------------------------------------
def autenticar_usuario(email, senha_digitada):
    """Verifica se o email existe e se o hash da senha corresponde."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Busca o hash salvo no banco
        cursor.execute("SELECT id, email, senha, nome, funcao FROM usuarios WHERE email = ?", (email,))
        usuario_db = cursor.fetchone()
        
        if usuario_db:
            # usuario_db é uma tupla: (id, email, hash_salvo, nome, funcao)
            hash_salvo = usuario_db[2] 
            
            # 2. Gera o hash da senha digitada pelo usuário
            hash_digitado = hash_senha(senha_digitada)
            
            # 3. Compara os hashes
            if hash_digitado == hash_salvo:
                # Se os hashes baterem, retorna todos os dados do usuário
                return {
                    'id': usuario_db[0],
                    'email': usuario_db[1],
                    'nome': usuario_db[3],
                    'funcao': usuario_db[4]
                }
            
        return None # Usuário não encontrado ou senha incorreta

    except Exception as e:
        print(f"Erro na autenticação: {e}")
        return None
    finally:
        if conn:
            conn.close()