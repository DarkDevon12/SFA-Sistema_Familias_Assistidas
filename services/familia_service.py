# services/familia_service.py
from database.db import get_connection
from models.familia import Familia

def criar_familia(responsavel, endereco, telefone, email, necessidades):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO familias (responsavel, endereco, telefone, email, necessidades)
        VALUES (?, ?, ?, ?, ?)
    """, (responsavel, endereco, telefone, email, necessidades))
    conn.commit()
    conn.close()

def listar_familias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM familias")
    rows = cursor.fetchall()
    conn.close()
    return [Familia(*r) for r in rows]

def buscar_familia_por_id(familia_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM familias WHERE id = ?", (familia_id,))
    row = cursor.fetchone()
    conn.close()
    return Familia(*row) if row else None

def atualizar_familia(familia_id, responsavel, endereco, telefone, email, necessidades):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE familias
        SET responsavel = ?, endereco = ?, telefone = ?, email = ?, necessidades = ?
        WHERE id = ?
    """, (responsavel, endereco, telefone, email, necessidades, familia_id))
    conn.commit()
    conn.close()

def excluir_familia(familia_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM familias WHERE id = ?", (familia_id,))
    conn.commit()
    conn.close()
