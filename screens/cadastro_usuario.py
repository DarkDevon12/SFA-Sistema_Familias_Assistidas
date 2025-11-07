# screens/cadastro_usuario.py

import tkinter as tk
from tkinter import messagebox
from services.usuario_service import criar_novo_usuario

def mostrar_tela_cadastro():
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastrar Novo Usuário")
    janela_cadastro.geometry("400x350")

    nome_var = tk.StringVar()
    email_var = tk.StringVar()
    senha_var = tk.StringVar()
    confirmar_senha_var = tk.StringVar()

    def handle_cadastro():
        nome = nome_var.get()
        email = email_var.get()
        senha = senha_var.get()
        confirmar_senha = confirmar_senha_var.get()

        if not nome or not email or not senha:
            messagebox.showwarning("Campos obrigatórios", "Todos os campos são obrigatórios.")
            return

        if senha != confirmar_senha:
            messagebox.showerror("Erro de Cadastro", "As senhas não conferem.")
            return

        try:
            resultado = criar_novo_usuario(nome, email, senha)
            if "sucesso" in resultado.lower():
                messagebox.showinfo("Sucesso", resultado)
                janela_cadastro.destroy()
            else:
                messagebox.showerror("Erro", resultado)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar: {str(e)}")

    tk.Label(janela_cadastro, text="Nome:").pack(pady=5)
    tk.Entry(janela_cadastro, textvariable=nome_var, width=40).pack()

    tk.Label(janela_cadastro, text="Email (login):").pack(pady=5)
    tk.Entry(janela_cadastro, textvariable=email_var, width=40).pack()

    tk.Label(janela_cadastro, text="Senha:").pack(pady=5)
    tk.Entry(janela_cadastro, textvariable=senha_var, show="*", width=40).pack()

    tk.Label(janela_cadastro, text="Confirmar Senha:").pack(pady=5)
    tk.Entry(janela_cadastro, textvariable=confirmar_senha_var, show="*", width=40).pack()

    tk.Button(janela_cadastro, text="Cadastrar", command=handle_cadastro).pack(pady=20)

    janela_cadastro.transient(janela_cadastro.master)
    janela_cadastro.grab_set()
    janela_cadastro.wait_window()
