from database.db import get_connection

class Membro:
    def __init__(self, id, id_familia, nome, idade, relacao):
        self.id = id
        self.id_familia = id_familia
        self.nome = nome
        self.idade = idade
        self.relacao = relacao

    def __repr__(self):
        return f"<Membro {self.nome} da familia {self.id_familia}>"

def listar_membros(familia_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM membros_familia WHERE id_familia = ?", (familia_id,))
    rows = cursor.fetchall()
    conn.close()
    return [Membro(*r) for r in rows]

if __name__ == "__main__":
    membros = listar_membros(1)
    print(membros)
