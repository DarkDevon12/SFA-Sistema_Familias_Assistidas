# models/usuario.py (Código CORRIGIDO)

from database.db import get_connection

class Usuario:
    # A senha FOI REMOVIDA dos atributos da classe
    def __init__(self, id, nome, email, funcao):
        self.id = id
        self.nome = nome
        self.email = email
        # self.senha foi removido
        self.funcao = funcao

    def __repr__(self):
        return f"<Usuario {self.nome} ({self.funcao})>"

# Função separada para listar usuários no banco
def listar_usuarios():
    # NOTA: O 'SELECT *' ainda puxa a senha. 
    # Para evitar isso, use SELECT id, nome, email, funcao FROM usuarios
    conn = get_connection()
    cursor = conn.cursor()
    
    # Para fins de demonstração, vamos apenas listar os dados necessários
    cursor.execute("SELECT id, nome, email, funcao FROM usuarios") 
    rows = cursor.fetchall()
    conn.close()
    
    # O *r aqui funciona, pois a ordem dos dados no banco e no construtor são iguais
    return [Usuario(*r) for r in rows] 

# Apenas para teste rápido (pode remover depois)
if __name__ == "__main__":
    # Este bloco também deve ser atualizado para a nova estrutura do construtor
    try:
        usuarios = listar_usuarios()
        print(usuarios)
    except Exception as e:
        print(f"Erro ao listar usuários (verifique se o banco foi inicializado): {e}")