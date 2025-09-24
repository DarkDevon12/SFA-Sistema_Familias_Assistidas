from database.db import get_connection

class Familia:
    def __init__(self, id, responsavel, endereco, telefone, email, necessidades):
        self.id = id
        self.responsavel = responsavel
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.necessidades = necessidades

    def __repr__(self):
        return f"<Familia {self.responsavel}>"

def listar_familias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM familias")
    rows = cursor.fetchall()
    conn.close()
    return [Familia(*r) for r in rows]

if __name__ == "__main__":
    familias = listar_familias()
    print(familias)
