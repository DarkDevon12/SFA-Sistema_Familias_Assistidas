import tkinter as tk
from database.db import get_connection

def abrir_atendimento():
    janela = tk.Tk()
    janela.title("Registro de Atendimento")

    tk.Label(janela, text="Nome da Família:").pack()
    entry_familia_id = tk.Entry(janela)
    entry_familia_id.pack()

    tk.Label(janela, text="Data:").pack()
    entry_data = tk.Entry(janela)
    entry_data.pack()

    tk.Label(janela, text="Tipo de auxílio:").pack()
    entry_tipo = tk.Entry(janela)
    entry_tipo.pack()

    tk.Label(janela, text="Observações:").pack()
    entry_observacoes = tk.Entry(janela)
    entry_observacoes.pack()

    tk.Label(janela, text="Retorno previsto:").pack()
    entry_retorno = tk.Entry(janela)
    entry_retorno.pack()

    tk.Label(janela, text="ID do Usuário:").pack()
    entry_usuario_id = tk.Entry(janela)
    entry_usuario_id.pack()

    label_resultado = tk.Label(janela, text="")
    label_resultado.pack()

    def registrar_atendimento():
        familia_id = entry_familia_id.get()
        data = entry_data.get()
        tipo_auxilio = entry_tipo.get()
        observacoes = entry_observacoes.get()
        retorno_previsto = entry_retorno.get()
        usuario_id = entry_usuario_id.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO atendimentos (id_familia, data, tipo_auxilio, observacoes, retorno_previsto, id_usuario) VALUES (?, ?, ?, ?, ?, ?)",
            (familia_id, data, tipo_auxilio, observacoes, retorno_previsto, usuario_id)
        )
        conn.commit()
        conn.close()
        label_resultado.config(text="Atendimento registrado com sucesso!")

    tk.Button(janela, text="Registrar", command=registrar_atendimento).pack(pady=10)

    janela.mainloop()
