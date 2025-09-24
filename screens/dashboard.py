# screens/dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox
from screens.cadastro_familia import abrir_cadastro
from screens.atendimentos import abrir_atendimento
from services.familia_service import listar_familias, excluir_familia, atualizar_familia


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

    # ---------------------------
    # Função para abrir lista de famílias cadastradas
    # ---------------------------
    def abrir_lista_familias():
        janela_familias = tk.Toplevel()
        janela_familias.title("Famílias Cadastradas")
        janela_familias.geometry("700x400")

        colunas = ("ID", "Responsável", "Endereço", "Telefone", "Email", "Necessidades")
        tree = ttk.Treeview(janela_familias, columns=colunas, show="headings")
        tree.pack(fill="both", expand=True)

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Carregar dados
        def carregar_familias():
            for item in tree.get_children():
                tree.delete(item)
            familias = listar_familias()
            for f in familias:
                tree.insert("", "end", values=(f.id, f.responsavel, f.endereco, f.telefone, f.email, f.necessidades))

        carregar_familias()

        # ---------------------------
        # Função para editar família
        # ---------------------------
        def editar():
            selecionado = tree.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione uma família para editar.")
                return
            item = tree.item(selecionado[0])
            familia_id, responsavel, endereco, telefone, email, necessidades = item["values"]

            # Nova janela de edição
            edit_win = tk.Toplevel(janela_familias)
            edit_win.title("Editar Família")
            edit_win.geometry("400x350")

            tk.Label(edit_win, text="Responsável:").pack()
            entry_responsavel = tk.Entry(edit_win)
            entry_responsavel.insert(0, responsavel)
            entry_responsavel.pack()

            tk.Label(edit_win, text="Endereço:").pack()
            entry_endereco = tk.Entry(edit_win)
            entry_endereco.insert(0, endereco)
            entry_endereco.pack()

            tk.Label(edit_win, text="Telefone:").pack()
            entry_telefone = tk.Entry(edit_win)
            entry_telefone.insert(0, telefone)
            entry_telefone.pack()

            tk.Label(edit_win, text="Email:").pack()
            entry_email = tk.Entry(edit_win)
            entry_email.insert(0, email)
            entry_email.pack()

            tk.Label(edit_win, text="Necessidades:").pack()
            entry_necessidades = tk.Entry(edit_win)
            entry_necessidades.insert(0, necessidades)
            entry_necessidades.pack()

            def salvar_edicao():
                novos_dados = {
                    "responsavel": entry_responsavel.get(),
                    "endereco": entry_endereco.get(),
                    "telefone": entry_telefone.get(),
                    "email": entry_email.get(),
                    "necessidades": entry_necessidades.get()
                }
                atualizar_familia(familia_id, novos_dados)
                carregar_familias()
                messagebox.showinfo("Sucesso", "Família atualizada com sucesso!")
                edit_win.destroy()

            tk.Button(edit_win, text="Salvar", command=salvar_edicao).pack(pady=10)

        # ---------------------------
        # Frame de botões
        # ---------------------------
        frame_botoes = tk.Frame(janela_familias)
        frame_botoes.pack(fill="x", pady=10)

        tk.Button(frame_botoes, text="Editar", command=editar).pack(side="right", padx=5)
        tk.Button(frame_botoes, text="Excluir", command=lambda: deletar()).pack(side="right", padx=5)
        tk.Button(frame_botoes, text="Atualizar Lista", command=carregar_familias).pack(side="right", padx=5)

        # Função excluir (fica no final para acessar carregar_familias)
        def deletar():
            selecionado = tree.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione uma família para excluir.")
                return
            item = tree.item(selecionado[0])
            familia_id = item["values"][0]
            excluir_familia(familia_id)
            carregar_familias()
            messagebox.showinfo("Sucesso", "Família excluída com sucesso.")

    # ---------------------------
    # Botões principais da dashboard
    # ---------------------------
    tk.Button(janela, text="Cadastrar Família", width=25, command=abrir_cadastro).pack(pady=5)
    tk.Button(janela, text="Registrar Atendimento", width=25, command=abrir_atendimento).pack(pady=5)
    tk.Button(janela, text="Famílias já cadastradas", width=25, command=abrir_lista_familias).pack(pady=5)

    janela.mainloop()
