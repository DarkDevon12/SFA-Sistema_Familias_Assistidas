# screens/login.py
import tkinter as tk
from screens.dashboard import abrir_dashboard
from models.usuario import listar_usuarios

def verificar_login(email, senha):
    usuarios = listar_usuarios()
    for u in usuarios:
        if u.email == email and u.senha == senha:
            return u
    return None

def abrir_login():
    login_janela = tk.Tk()
    login_janela.title("Login - Sistema de Famílias Assistidas")

    
    # Tamanho da janela
    login_janela.geometry("500x350")
    # Centralizar
    screen_width = login_janela.winfo_screenwidth()
    screen_height = login_janela.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 350) // 2
    login_janela.geometry(f"500x350+{x}+{y}")

    
    tk.Label(login_janela, text="Email:").pack()
    entry_email = tk.Entry(login_janela)
    entry_email.pack()

    tk.Label(login_janela, text="Senha:").pack()
    entry_senha = tk.Entry(login_janela, show="*")
    entry_senha.pack()

    label_resultado = tk.Label(login_janela, text="")
    label_resultado.pack()

    def entrar():
        email = entry_email.get()
        senha = entry_senha.get()
        usuario = verificar_login(email, senha)
        if usuario:
            login_janela.destroy()
            abrir_dashboard(usuario)  # abre dashboard
        else:
            label_resultado.config(text="Usuário ou senha incorretos.")

    tk.Button(login_janela, text="Entrar", command=entrar).pack(pady=10)
    login_janela.mainloop()
