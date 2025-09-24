import tkinter as tk
from models.familia import listar_familias
from models.atendimento import listar_atendimentos

def abrir_relatorios():
    janela = tk.Tk()
    janela.title("Relatórios")

    familias = listar_familias()
    tk.Label(janela, text=f"Total de famílias: {len(familias)}").pack()

    if familias:
        atendimentos = listar_atendimentos(familias[0].id)
        tk.Label(janela, text=f"Atendimentos da primeira família: {len(atendimentos)}").pack()

    janela.mainloop()
