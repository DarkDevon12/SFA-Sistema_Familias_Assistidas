# screens/dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox
from screens.cadastro_familia import abrir_cadastro
from screens.atendimentos import abrir_atendimento
from services.familia_service import listar_familias, excluir_familia, atualizar_familia
from models.usuario import Usuario
from screens.relatorios import RelatoriosWindow
from screens.alertas import AlertasWindow
from screens.historico_familia import HistoricoFamiliaWindow

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller, usuario_data):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.usuario = None
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.main_content = tk.Frame(self)
        self.main_content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self._setup_layout(self.main_content)
        self.atualizar_dados(usuario_data)

    def atualizar_dados(self, usuario_data):
        if usuario_data:
            self.usuario = Usuario(
                usuario_data['id'], 
                usuario_data['nome'], 
                usuario_data['email'], 
                usuario_data['funcao']
            )
            self.label_bem_vindo.config(text=f"Bem-vindo(a), {self.usuario.nome}!")
            self.label_funcao.config(text=f"Função no Sistema: {self.usuario.funcao}")

    def _setup_layout(self, parent_frame):
        def sair():
            self.controller.show_frame("Login")
        
        tk.Button(
            parent_frame,
            text="Sair",
            command=sair,
            bg="#C0392B", 
            fg="white"
        ).pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        self.label_bem_vindo = tk.Label(parent_frame, text="", font=("Arial", 16, "bold"))
        self.label_bem_vindo.pack(pady=(10, 5))
        
        self.label_funcao = tk.Label(parent_frame, text="", font=("Arial", 10))
        self.label_funcao.pack(pady=(0, 20))

        def abrir_lista_familias():
            janela_familias = tk.Toplevel(self.controller.master)
            janela_familias.title("Famílias Cadastradas")
            janela_familias.geometry("700x400")

            colunas = ("ID", "Responsável", "Endereço", "Telefone", "Email", "Necessidades")
            tree = ttk.Treeview(janela_familias, columns=colunas, show="headings")
            tree.pack(fill="both", expand=True)

            for col in colunas:
                tree.heading(col, text=col)
                tree.column(col, width=120)

            def carregar_familias():
                for item in tree.get_children():
                    tree.delete(item)
                familias = listar_familias()
                for f in familias:
                    tree.insert("", "end", values=(f.id, f.responsavel, f.endereco, f.telefone, f.email, f.necessidades))

            carregar_familias()

            def mostrar_historico():
                selecionado = tree.selection()
                if not selecionado:
                    messagebox.showwarning("Aviso", "Selecione uma família para ver o histórico.")
                    return
                item = tree.item(selecionado[0])
                familia_id = item["values"][0]
                nome = item["values"][1]
                HistoricoFamiliaWindow(janela_familias, id_familia=familia_id, nome_familia=nome)

            def deletar():
                selecionado = tree.selection()
                if not selecionado:
                    messagebox.showwarning("Aviso", "Selecione uma família para excluir.")
                    return
                
                confirmar = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta família?")
                if confirmar:
                    item = tree.item(selecionado[0])
                    familia_id = item["values"][0]
                    excluir_familia(familia_id)
                    carregar_familias()
                    messagebox.showinfo("Sucesso", "Família excluída com sucesso.")
            
            def editar():
                selecionado = tree.selection()
                if not selecionado:
                    messagebox.showwarning("Aviso", "Selecione uma família para editar.")
                    return
                item = tree.item(selecionado[0])
                familia_id, responsavel, endereco, telefone, email, necessidades = item["values"]

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

            frame_botoes = tk.Frame(janela_familias)
            frame_botoes.pack(fill="x", pady=10)

            tk.Button(frame_botoes, text="Editar", command=editar).pack(side="right", padx=5)
            tk.Button(frame_botoes, text="Excluir", command=deletar).pack(side="right", padx=5)
            tk.Button(frame_botoes, text="Atualizar Lista", command=carregar_familias).pack(side="right", padx=5)
            tk.Button(frame_botoes, text="Histórico", command=mostrar_historico).pack(side="right", padx=5)

        tk.Button(parent_frame, text="Cadastrar Família", width=25, 
                  command=lambda: abrir_cadastro(self.controller.master)).pack(pady=5)
                  
        tk.Button(parent_frame, text="Registrar Atendimento", width=25, 
                  command=lambda: abrir_atendimento(self.controller.master, self.usuario)).pack(pady=5)

        tk.Button(parent_frame, text="Famílias já cadastradas", width=25, 
                  command=abrir_lista_familias).pack(pady=5)

        tk.Button(parent_frame, text="Relatórios", width=25,
                  command=lambda: RelatoriosWindow(self.controller.master)).pack(pady=5)

        tk.Button(parent_frame, text="Ver Alertas Pendentes", width=25, 
                  command=lambda: AlertasWindow(self.controller.master, dias=3)).pack(pady=5)
