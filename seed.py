from database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO usuarios (nome, email, senha, funcao)
VALUES (?, ?, ?, ?)
""", ("Admin Teste", "admin@teste.com", "123456", "admin"))

conn.commit()
conn.close()
print("Usuário criado com sucesso!")
