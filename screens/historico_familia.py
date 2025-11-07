# screens/historico_familia.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.relatorio_service import historico_por_familia

class HistoricoFamiliaWindow(tk.Toplevel):
    def __init__(self, master=None, id_familia=None, nome_familia=""):
        super().__init__(master)
        self.title(f"Histórico da Família: {nome_familia}")
        self.geometry("850x500")

        cols = ("ID", "Data", "Tipo auxílio", "Observações", "Retorno previsto", "ID Usuário")
        self.tv = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tv.heading(c, text=c)
            self.tv.column(c, width=140)
        self.tv.pack(fill="both", expand=True)

        if id_familia is not None:
            self.atualizar(id_familia)

    def atualizar(self, id_familia):
        for r in self.tv.get_children():
            self.tv.delete(r)
        rows = historico_por_familia(id_familia)
        if not rows:
            messagebox.showinfo("Histórico", "Nenhum atendimento registrado para esta família.")
            return
        for row in rows:
            self.tv.insert("", "end", values=row)
