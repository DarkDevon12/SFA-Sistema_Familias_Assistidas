import tkinter as tk
from database.db import get_connection

def abrir_cadastro():
    janela = tk.Tk()
    janela.title("Cadastro de Família")

    tk.Label(janela, text="Responsável:").pack()
    entry_responsavel = tk.Entry(janela)
    entry_responsavel.pack()

    tk.Label(janela, text="Endereço:").pack()
    entry_endereco = tk.Entry(janela)
    entry_endereco.pack()

    tk.Label(janela, text="Telefone:").pack()
    entry_telefone = tk.Entry(janela)
    entry_telefone.pack()

    tk.Label(janela, text="Email:").pack()
    entry_email = tk.Entry(janela)
    entry_email.pack()

    tk.Label(janela, text="Necessidades:").pack()
    entry_necessidades = tk.Entry(janela)
    entry_necessidades.pack()

    label_resultado = tk.Label(janela, text="")
    label_resultado.pack()

    def salvar_familia():
        responsavel = entry_responsavel.get()
        endereco = entry_endereco.get()
        telefone = entry_telefone.get()
        email = entry_email.get()
        necessidades = entry_necessidades.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO familias (responsavel, endereco, telefone, email, necessidades) VALUES (?, ?, ?, ?, ?)",
            (responsavel, endereco, telefone, email, necessidades)
        )
        conn.commit()
        conn.close()
        label_resultado.config(text="Família cadastrada com sucesso!")

    tk.Button(janela, text="Salvar", command=salvar_familia).pack(pady=10)

    janela.mainloop()
