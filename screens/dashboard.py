# screens/dashboard.py
import tkinter as tk
from models.familia import listar_familias
from screens.cadastro_familia import abrir_cadastro
from screens.atendimentos import abrir_atendimento

def abrir_dashboard(usuario):
    # Cria a janela principal da dashboard
    janela = tk.Tk()
    janela.title(f"Dashboard - Bem-vindo {usuario.nome}")
    largura = 500
    altura = 350

    # Centralizar na tela
    screen_width = janela.winfo_screenwidth()
    screen_height = janela.winfo_screenheight()
    x = (screen_width - largura) // 2
    y = (screen_height - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

    tk.Label(janela, text=f"Bem-vindo, {usuario.nome}!", font=("Arial", 14)).pack(pady=10)

    # Função para abrir lista de famílias cadastradas
    def abrir_lista_familias():
        familias = listar_familias()
        janela_familias = tk.Toplevel()
        janela_familias.title("Famílias Cadastradas")
        janela_familias.geometry("600x400")

        if not familias:
            tk.Label(janela_familias, text="Nenhuma família cadastrada.").pack(pady=10)
            return

        # Cabeçalho
        tk.Label(janela_familias, text="Lista de Famílias", font=("Arial", 12, "bold")).pack(pady=5)

        # Exibe cada família em um label formatado
        for f in familias:
            texto = (
                f"Responsável: {f.responsavel}\n"
                f"Endereço: {f.endereco}\n"
                f"Telefone: {f.telefone}\n"
                f"Necessidades: {f.necessidades if f.necessidades else 'Não informado'}"
            )
            frame = tk.Frame(janela_familias, relief="groove", borderwidth=2, padx=10, pady=5)
            frame.pack(fill="x", padx=10, pady=5)

            tk.Label(frame, text=texto, justify="left", anchor="w").pack(fill="x")

    # Botões principais da dashboard
    tk.Button(janela, text="Cadastrar Família", width=25, command=abrir_cadastro).pack(pady=5)
    tk.Button(janela, text="Registrar Atendimento", width=25, command=abrir_atendimento).pack(pady=5)
    tk.Button(janela, text="Famílias já cadastradas", width=25, command=abrir_lista_familias).pack(pady=5)

    janela.mainloop()
