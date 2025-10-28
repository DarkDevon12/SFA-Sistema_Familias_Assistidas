# screens/login.py

import tkinter as tk
from tkinter import messagebox
# Remova: from screens.dashboard import abrir_dashboard (Não é mais necessário)
from services.usuario_service import autenticar_usuario 
from screens.cadastro_usuario import mostrar_tela_cadastro
from models.usuario import Usuario 


class LoginFrame(tk.Frame):
    """
    Representa a tela de Login como um Frame que será exibido 
    dentro da janela principal do aplicativo.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller # O objeto AppPrincipal

        # Configura para centralizar o conteúdo no Frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Cria um Frame interno para organizar e centralizar os widgets de login
        self.content_frame = tk.Frame(self)
        self.content_frame.grid(row=0, column=0, padx=10, pady=10)

        # ------------------------------------------------
        # LAYOUT DE LOGIN
        # ------------------------------------------------
        
        tk.Label(self.content_frame, text="SFA - LOGIN", font=("Arial", 16, "bold")).pack(pady=(20, 15))
        
        tk.Label(self.content_frame, text="Email:").pack()
        self.entry_email = tk.Entry(self.content_frame, width=30)
        self.entry_email.pack()

        tk.Label(self.content_frame, text="Senha:").pack()
        self.entry_senha = tk.Entry(self.content_frame, show="*", width=30)
        self.entry_senha.pack()

        self.label_resultado = tk.Label(self.content_frame, text="", fg="red")
        self.label_resultado.pack()

        tk.Button(self.content_frame, text="Entrar", command=self.entrar).pack(pady=10)
        
        # O cadastro de usuário pode continuar abrindo uma nova janela (Toplevel)
        tk.Button(self.content_frame, text="Criar Usuário", command=mostrar_tela_cadastro).pack(pady=5)


    def verificar_login(self, email, senha):
        """Usa o serviço para autenticar a senha hasheada e retorna os dados do usuário."""
        # A função de autenticação retorna um dicionário com os dados do usuário ou None.
        dados_usuario = autenticar_usuario(email, senha) 
        return dados_usuario # Retorna o dicionário completo


    def entrar(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        
        usuario_data = self.verificar_login(email, senha)
        
        if usuario_data:
            self.label_resultado.config(text="")
            # Login bem-sucedido: Chama o controlador para trocar para o Dashboard
            self.controller.show_frame("Dashboard", user_data=usuario_data)
        else:
            self.label_resultado.config(text="Usuário ou senha incorretos.")

# O arquivo NÃO contem mais: abrir_login() nem login_janela.mainloop()