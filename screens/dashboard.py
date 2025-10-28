# screens/dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox
# Importações relativas (ajustadas para funcionar dentro do Frame)
from screens.cadastro_familia import abrir_cadastro
from screens.atendimentos import abrir_atendimento
from services.familia_service import listar_familias, excluir_familia, atualizar_familia
from models.usuario import Usuario 
# Não precisamos importar o login aqui, o AppPrincipal gerencia.

class DashboardFrame(tk.Frame):
    """
    Representa a tela principal (Dashboard) como um Frame,
    permitindo transição na mesma janela.
    """
    def __init__(self, parent, controller, usuario_data):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # O objeto do usuário será criado ou atualizado aqui
        self.usuario = None
        
        # Estrutura básica para garantir que o layout preencha a tela
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Cria um Frame interno para o conteúdo principal
        self.main_content = tk.Frame(self)
        self.main_content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Função para configurar o layout (Chamada única)
        self._setup_layout(self.main_content)
        
        # Atualiza os dados do usuário assim que o Frame é criado
        self.atualizar_dados(usuario_data)

    def atualizar_dados(self, usuario_data):
        """Atualiza a instância do usuário e os labels de boas-vindas."""
        if usuario_data:
            # Cria a instância do Usuario a partir dos dados do dicionário
            self.usuario = Usuario(
                usuario_data['id'], 
                usuario_data['nome'], 
                usuario_data['email'], 
                usuario_data['funcao']
            )
            self.label_bem_vindo.config(text=f"Bem-vindo(a), {self.usuario.nome}!")
            self.label_funcao.config(text=f"Função no Sistema: {self.usuario.funcao}")


    def _setup_layout(self, parent_frame):
        """Configura o layout visual do Dashboard, incluindo o botão Sair e os botões principais."""
        
        # -----------------------------------------------------------
        # FUNÇÃO DE SAÍDA (LOGOUT)
        # -----------------------------------------------------------
        def sair():
            # Usa o controller para voltar para a tela de Login
            self.controller.show_frame("Login")
        
        # -----------------------------------------------------------
        # BOTÃO DE SAIR - POSICIONADO NO TOPO/DIREITA
        # -----------------------------------------------------------
        tk.Button(
            parent_frame,
            text="Sair",
            command=sair,
            bg="#C0392B", 
            fg="white"
        ).pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)
        
        # Labels de Usuário (Serão atualizados pelo self.atualizar_dados)
        self.label_bem_vindo = tk.Label(parent_frame, text="", font=("Arial", 16, "bold"))
        self.label_bem_vindo.pack(pady=(10, 5))
        
        self.label_funcao = tk.Label(parent_frame, text="", font=("Arial", 10))
        self.label_funcao.pack(pady=(0, 20))


        # ---------------------------
        # Função para abrir lista de famílias cadastradas
        # ---------------------------
        def abrir_lista_familias():
            # Usa o master do AppPrincipal como pai, para garantir que fique por cima
            janela_familias = tk.Toplevel(self.controller.master)
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
            # Função excluir
            # ---------------------------
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
            
            # ---------------------------
            # Frame de botões
            # ---------------------------
            frame_botoes = tk.Frame(janela_familias)
            frame_botoes.pack(fill="x", pady=10)

            tk.Button(frame_botoes, text="Editar", command=editar).pack(side="right", padx=5)
            tk.Button(frame_botoes, text="Excluir", command=deletar).pack(side="right", padx=5)
            tk.Button(frame_botoes, text="Atualizar Lista", command=carregar_familias).pack(side="right", padx=5)
            
            janela_familias.mainloop()


        # ---------------------------
        # Botões principais da dashboard (Frame) - CORRIGIDOS
        # ---------------------------
        # A lambda passa self.controller.master (a janela raiz) como argumento para as funções
        # que criam janelas Toplevel, garantindo que elas abram corretamente.
        tk.Button(
            parent_frame, 
            text="Cadastrar Família", 
            width=25, 
            command=lambda: abrir_cadastro(self.controller.master)
        ).pack(pady=5)
        
        tk.Button(
            parent_frame, 
            text="Registrar Atendimento", 
            width=25, 
            command=lambda: abrir_atendimento(self.controller.master)
        ).pack(pady=5)
        
        tk.Button(parent_frame, text="Famílias já cadastradas", width=25, command=abrir_lista_familias).pack(pady=5)