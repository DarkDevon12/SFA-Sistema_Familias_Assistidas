import tkinter as tk
from tkinter import ttk, messagebox
from services.familia_service import listar_familias, excluir_familia

def abrir_familias():
    janela = tk.Toplevel()
    janela.title("Famílias Cadastradas")
    janela.geometry("700x400")

    # Tabela
    colunas = ("ID", "Responsável", "Endereço", "Telefone", "Email", "Necessidades")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    tree.pack(fill="both", expand=True)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    # Função para carregar os dados
    def carregar_familias():
        for item in tree.get_children():
            tree.delete(item)
        familias = listar_familias()
        for f in familias:
            tree.insert("", "end", values=(f.id, f.responsavel, f.endereco, f.telefone, f.email, f.necessidades))

    carregar_familias()

    # Botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(fill="x", pady=10)

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

    tk.Button(frame_botoes, text="Excluir", command=deletar).pack(side="right", padx=5)

    tk.Button(frame_botoes, text="Atualizar Lista", command=carregar_familias).pack(side="right", padx=5)

    janela.mainloop()
