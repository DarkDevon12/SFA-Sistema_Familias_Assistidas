# screens/app_principal.py

import tkinter as tk
# Importações necessárias:
from screens.login import LoginFrame 
from screens.dashboard import DashboardFrame 
from models.usuario import Usuario

class AppPrincipal:
    """Gerencia a janela principal e a navegação entre os Frames."""
    
    def __init__(self, master):
        self.master = master
        master.title("SFA - Sistema de Famílias Assistidas")
        
        # O container principal onde todos os Frames serão empilhados
        self.container = tk.Frame(master)
        self.container.pack(side="top", fill="both", expand=True)
        
        # Garante que o Frame preencha o container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dicionário para armazenar as instâncias dos Frames
        self.frames = {}
        
        # Inicialização do Frame de Login
        self.frames["Login"] = LoginFrame(parent=self.container, controller=self)
        self.frames["Login"].grid(row=0, column=0, sticky="nsew")
        
        # Exibe a primeira tela
        self.show_frame("Login")

    def show_frame(self, page_name, user_data=None):
        """Alterna entre as telas (Frames)."""
        
        # Lógica para inicializar ou atualizar o Dashboard
        if page_name == "Dashboard":
            # Se o Dashboard ainda não existe, cria ele.
            if page_name not in self.frames:
                self.frames["Dashboard"] = DashboardFrame(
                    parent=self.container, 
                    controller=self, 
                    usuario_data=user_data
                )
                self.frames["Dashboard"].grid(row=0, column=0, sticky="nsew")
            else:
                # Se o Dashboard já existe (ex: voltando do login), apenas atualiza
                self.frames["Dashboard"].atualizar_dados(user_data)
        
        frame = self.frames[page_name]
        frame.tkraise() # Coloca o Frame desejado no topo da pilha