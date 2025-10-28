import tkinter as tk
from tkinter import messagebox
from services.usuario_service import criar_novo_usuario

# Supondo que você tem uma função principal para mostrar a tela
def mostrar_tela_cadastro():
    
    # 1. Configurar a Janela
    janela_cadastro = tk.Toplevel() # Toplevel cria uma nova janela flutuante
    janela_cadastro.title("Cadastrar Novo Usuário")
    janela_cadastro.geometry("400x250")

    # Variáveis para armazenar os inputs
    nome_var = tk.StringVar()
    email_var = tk.StringVar()
    senha_var = tk.StringVar()

    def handle_cadastro():
        """Função chamada ao clicar no botão Cadastrar."""
        nome = nome_var.get()
        email = email_var.get()
        senha = senha_var.get()
        
        if not nome or not email or not senha:
            messagebox.showerror("Erro de Cadastro", "Todos os campos são obrigatórios.")
            return

        # Chama a função de serviço (Passo 1)
        resultado = criar_novo_usuario(nome, email, senha)
        
        if "sucesso" in resultado:
            messagebox.showinfo("Sucesso", resultado)
            janela_cadastro.destroy() # Fecha a janela de cadastro
        else:
            messagebox.showerror("Erro", resultado)

    # 2. Layout (Elementos da Tela)
    
    tk.Label(janela_cadastro, text="Nome:").pack(pady=5)
    tk.Entry(janela_cadastro, textvariable=nome_var, width=40).pack()

    tk.Label(janela_cadastro, text="Login:").pack(pady=5)
    tk.Entry(janela_cadastro, textvariable=email_var, width=40).pack()

    tk.Label(janela_cadastro, text="Senha:").pack(pady=5)
    # Mostra * (asteriscos) ao digitar a senha
    tk.Entry(janela_cadastro, textvariable=senha_var, show="*", width=40).pack()
    
    # Botão de Ação
    tk.Button(janela_cadastro, text="Cadastrar", command=handle_cadastro).pack(pady=10)
    
    janela_cadastro.transient(janela_cadastro.master) # Mantém no topo da janela principal
    janela_cadastro.grab_set() # Desabilita interação com outras janelas
    janela_cadastro.wait_window() # Espera o fechamento da janela
    
# Se você quiser testar esta tela separadamente:
# if __name__ == "__main__":
#     root = tk.Tk()
#     mostrar_tela_cadastro()
#     root.mainloop()