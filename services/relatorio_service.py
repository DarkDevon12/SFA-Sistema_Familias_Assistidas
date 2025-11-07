# services/relatorio_service.py
from database.db import get_connection
from collections import Counter
from datetime import datetime, timedelta

def listar_familias_simples():
    """Retorna tuplas (id, responsavel, endereco, telefone, email, necessidades)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, responsavel, endereco, telefone, email, necessidades FROM familias")
    rows = cur.fetchall()
    conn.close()
    return rows

def frequencia_atendimentos():
    """Retorna lista de (familia_id, responsavel, total_atendimentos) ordenado por total desc."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.id, f.responsavel, COUNT(a.id) as total
        FROM familias f
        LEFT JOIN atendimentos a ON a.id_familia = f.id
        GROUP BY f.id
        ORDER BY total DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def necessidades_mais_comuns(limit=50):
    """Assume campo 'necessidades' como texto com separador vírgula."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT necessidades FROM familias WHERE necessidades IS NOT NULL AND necessidades != ''")
    rows = cur.fetchall()
    conn.close()
    counter = Counter()
    for (txt,) in rows:
        parts = [p.strip().lower() for p in txt.split(',') if p and p.strip()]
        counter.update(parts)
    return counter.most_common(limit)

def alertas_retorno_proximos(dias=3):
    """
    Retorna lista de tuplas (id_atendimento, id_familia, responsavel, data, retorno_previsto)
    cujo retorno_previsto esteja até (hoje + dias).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, f.id, f.responsavel, a.data, a.retorno_previsto
        FROM atendimentos a
        JOIN familias f ON f.id = a.id_familia
        WHERE a.retorno_previsto IS NOT NULL AND a.retorno_previsto != ''
        ORDER BY a.retorno_previsto ASC
    """)
    rows = cur.fetchall()
    conn.close()

    results = []
    now = datetime.now().date()
    limite = now + timedelta(days=dias)
    for row in rows:
        rp = row[4]
        # tenta parsear ISO 'YYYY-MM-DD' e outras variações
        try:
            rp_dt = datetime.fromisoformat(rp).date()
        except Exception:
            # tenta DD/MM/YYYY
            try:
                rp_dt = datetime.strptime(rp, "%d/%m/%Y").date()
            except Exception:
                continue
        if rp_dt <= limite:
            results.append((row[0], row[1], row[2], row[3], rp))
    return results

def historico_por_familia(id_familia):
    """Retorna atendimentos da familia ordenados por data desc (tuplas)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, data, tipo_auxilio, observacoes, retorno_previsto, id_usuario
        FROM atendimentos
        WHERE id_familia = ?
        ORDER BY data DESC
    """, (id_familia,))
    rows = cur.fetchall()
    conn.close()
    return rows
