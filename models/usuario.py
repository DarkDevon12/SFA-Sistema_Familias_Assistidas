# models/usuario.py

from database.db import get_connection

class Usuario:
    def __init__(self, id, nome, email, senha, funcao):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.funcao = funcao

    def __repr__(self):
        return f"<Usuario {self.nome} ({self.funcao})>"

# Função separada para listar usuários no banco
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()
    conn.close()
    return [Usuario(*r) for r in rows]

# Apenas para teste rápido (pode remover depois)
if __name__ == "__main__":
    usuarios = listar_usuarios()
    print(usuarios)
