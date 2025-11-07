# screens/cadastro_familia.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.familia_service import criar_familia
from database.db import get_connection

def abrir_cadastro(master):
    janela = tk.Toplevel(master)
    janela.title("Cadastro de Família")
    janela.geometry("600x700")

    # ----------------------------
    # Frame com Scrollbar
    # ----------------------------
    canvas = tk.Canvas(janela)
    scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ----------------------------
    # Cabeçalho
    # ----------------------------
    tk.Label(scroll_frame, text="Cadastro de Família", font=("Arial", 16, "bold")).pack(pady=10)

    # ----------------------------
    # Dados da Família
    # ----------------------------
    frame_dados = tk.LabelFrame(scroll_frame, text="Dados do Responsável", padx=10, pady=10)
    frame_dados.pack(fill="x", padx=20, pady=10)

    tk.Label(frame_dados, text="Nome do Responsável:").pack(anchor="w")
    entry_responsavel = tk.Entry(frame_dados, width=60)
    entry_responsavel.pack()

    tk.Label(frame_dados, text="Endereço completo:").pack(anchor="w", pady=(10, 0))
    entry_endereco = tk.Entry(frame_dados, width=60)
    entry_endereco.pack()

    # ----------------------------
    # Contatos
    # ----------------------------
    frame_contato = tk.LabelFrame(scroll_frame, text="Contatos", padx=10, pady=10)
    frame_contato.pack(fill="x", padx=20, pady=10)

    tk.Label(frame_contato, text="Telefone:").pack(anchor="w")
    entry_telefone = tk.Entry(frame_contato, width=60)
    entry_telefone.pack()

    tk.Label(frame_contato, text="E-mail:").pack(anchor="w", pady=(10, 0))
    entry_email = tk.Entry(frame_contato, width=60)
    entry_email.pack()

    # ----------------------------
    # Membros da Família
    # ----------------------------
    frame_membros = tk.LabelFrame(scroll_frame, text="Membros da Família", padx=10, pady=10)
    frame_membros.pack(fill="x", padx=20, pady=10)

    membros_container = tk.Frame(frame_membros)
    membros_container.pack(fill="x")

    membros_entries = []

    def adicionar_membro():
        idx = len(membros_entries) + 1
        membro_frame = tk.Frame(membros_container, relief="groove", borderwidth=2, padx=5, pady=5)
        membro_frame.pack(fill="x", pady=5)

        tk.Label(membro_frame, text=f"Membro {idx}", font=("Arial", 10, "bold")).pack(anchor="w")

        tk.Label(membro_frame, text="Nome:").pack(anchor="w")
        nome = tk.Entry(membro_frame, width=40)
        nome.pack(anchor="w")

        tk.Label(membro_frame, text="Idade:").pack(anchor="w")
        idade = tk.Entry(membro_frame, width=10)
        idade.pack(anchor="w")

        tk.Label(membro_frame, text="Relação (ex: filho, mãe, etc.):").pack(anchor="w")
        relacao = tk.Entry(membro_frame, width=20)
        relacao.pack(anchor="w")

        membros_entries.append((membro_frame, nome, idade, relacao))

    def remover_membro():
        if membros_entries:
            frame, *_ = membros_entries.pop()
            frame.destroy()
        else:
            messagebox.showinfo("Aviso", "Nenhum membro para remover.")

    tk.Button(frame_membros, text="Adicionar Membro", command=adicionar_membro, bg="#2980B9", fg="white").pack(side="left", padx=5, pady=5)
    tk.Button(frame_membros, text="Remover Último", command=remover_membro, bg="#C0392B", fg="white").pack(side="left", padx=5, pady=5)

    # ----------------------------
    # Necessidades
    # ----------------------------
    frame_necessidades = tk.LabelFrame(scroll_frame, text="Principais Necessidades", padx=10, pady=10)
    frame_necessidades.pack(fill="x", padx=20, pady=10)

    necessidades_opcoes = ["Alimentação", "Saúde", "Educação", "Habitação", "Emprego", "Outros"]
    necessidades_vars = {opt: tk.BooleanVar() for opt in necessidades_opcoes}

    for opt in necessidades_opcoes:
        tk.Checkbutton(frame_necessidades, text=opt, variable=necessidades_vars[opt]).pack(anchor="w")

    # ----------------------------
    # Função de salvar
    # ----------------------------
    def salvar_familia():
        responsavel = entry_responsavel.get().strip()
        endereco = entry_endereco.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()

        if not responsavel or not endereco:
            messagebox.showwarning("Campos obrigatórios", "Nome do responsável e endereço são obrigatórios.")
            return

        necessidades_selecionadas = [opt for opt, var in necessidades_vars.items() if var.get()]
        necessidades_texto = ", ".join(necessidades_selecionadas) if necessidades_selecionadas else "Não informado"

        try:
            familia_id = criar_familia(responsavel, endereco, telefone, email, necessidades_texto)

            conn = get_connection()
            cursor = conn.cursor()

            for frame, nome_entry, idade_entry, relacao_entry in membros_entries:
                nome = nome_entry.get().strip()
                idade = idade_entry.get().strip()
                relacao = relacao_entry.get().strip()

                if nome:
                    cursor.execute(
                        "INSERT INTO membros_familia (id_familia, nome, idade, relacao) VALUES (?, ?, ?, ?)",
                        (familia_id, nome, idade, relacao)
                    )

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "✅ Família cadastrada com sucesso!")

            # Limpa os campos
            entry_responsavel.delete(0, tk.END)
            entry_endereco.delete(0, tk.END)
            entry_telefone.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            for opt in necessidades_opcoes:
                necessidades_vars[opt].set(False)
            for frame, *_ in membros_entries:
                frame.destroy()
            membros_entries.clear()

        except Exception as e:
            messagebox.showerror("Erro ao salvar", f"Ocorreu um erro:\n{str(e)}")

    # ----------------------------
    # Botão Salvar
    # ----------------------------
    tk.Button(scroll_frame, text="Salvar Família", command=salvar_familia, bg="#27AE60", fg="white", font=("Arial", 11, "bold")).pack(pady=20)

    janela.mainloop()
