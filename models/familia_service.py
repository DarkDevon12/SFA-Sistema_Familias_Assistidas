# services/familia_service.py
from database.db import get_connection
from models.familia import Familia


# Buscar todas as famílias
def listar_familias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, responsavel, endereco, telefone, email, necessidades FROM familias")
    rows = cursor.fetchall()
    conn.close()

    familias = [Familia(*row) for row in rows]
    return familias


# Criar nova família
def criar_familia(responsavel, endereco, telefone, email, necessidades):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO familias (responsavel, endereco, telefone, email, necessidades)
        VALUES (?, ?, ?, ?, ?)
    """, (responsavel, endereco, telefone, email, necessidades))

    conn.commit()
    conn.close()


# Atualizar dados de uma família
def atualizar_familia(familia_id, novos_dados):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE familias
        SET responsavel = ?, endereco = ?, telefone = ?, email = ?, necessidades = ?
        WHERE id = ?
    """, (
        novos_dados.get("responsavel"),
        novos_dados.get("endereco"),
        novos_dados.get("telefone"),
        novos_dados.get("email"),
        novos_dados.get("necessidades"),
        familia_id
    ))

    conn.commit()
    conn.close()


# Excluir família pelo ID
def excluir_familia(familia_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM familias WHERE id = ?", (familia_id,))
    conn.commit()
    conn.close()
