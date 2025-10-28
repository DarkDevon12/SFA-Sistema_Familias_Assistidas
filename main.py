# main.py

import tkinter as tk
from database.db import init_db, migrar_db
from screens.app_principal import AppPrincipal # NOVO IMPORT

# Lógica de Inicialização do Banco de Dados
init_db()
migrar_db()

# 1. Cria a Janela Principal (Única Instância tk.Tk)
root = tk.Tk()

# 2. Configuração de Tela Cheia/Maximizada
# Tenta maximizar a janela (Funciona na maioria dos SOs)
try:
    root.state('zoomed') 
except Exception:
    # Caso 'zoomed' falhe (SO Linux mais antigo, etc.), use tela cheia
    root.attributes('-fullscreen', True) 
    
# 3. Inicia o Gerenciador de Telas
app = AppPrincipal(root)

# 4. Inicia o loop do Tkinter
root.mainloop()