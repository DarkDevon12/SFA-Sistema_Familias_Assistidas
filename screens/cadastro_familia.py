# screens/cadastro_familia.py
import tkinter as tk
from services.familia_service import criar_familia

def abrir_cadastro():
    janela = tk.Toplevel()  # importante usar Toplevel em vez de Tk
    janela.title("Cadastro de Família")
    janela.geometry("400x400")

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

        if not responsavel or not endereco:
            label_resultado.config(text="⚠ Responsável e Endereço são obrigatórios!")
            return

        try:
            criar_familia(responsavel, endereco, telefone, email, necessidades)
            label_resultado.config(text="✅ Família cadastrada com sucesso!")
            # limpa os campos
            entry_responsavel.delete(0, tk.END)
            entry_endereco.delete(0, tk.END)
            entry_telefone.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_necessidades.delete(0, tk.END)
        except Exception as e:
            label_resultado.config(text=f"❌ Erro ao salvar: {e}")

    tk.Button(janela, text="Salvar", command=salvar_familia).pack(pady=10)

    janela.mainloop()
