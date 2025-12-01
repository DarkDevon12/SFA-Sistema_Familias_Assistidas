import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from services.relatorio_service import (
    listar_familias_simples,
    frequencia_atendimentos,
    necessidades_mais_comuns,
)
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from openpyxl import Workbook


class RelatoriosWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Relatórios")
        self.geometry("900x600")

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)

        self.tab_fam = ttk.Frame(nb)
        self.tab_freq = ttk.Frame(nb)
        self.tab_nec = ttk.Frame(nb)

        nb.add(self.tab_fam, text="Famílias atendidas")
        nb.add(self.tab_freq, text="Frequência de atendimentos")
        nb.add(self.tab_nec, text="Necessidades mais comuns")

        self._montar_tab_familias()
        self._montar_tab_frequencia()
        self._montar_tab_necessidades()

    # ------------------------------------------------------------------
    # ABA: FAMÍLIAS
    # ------------------------------------------------------------------
    def _montar_tab_familias(self):
        cols = ("ID", "Responsável", "Endereço", "Telefone", "Email", "Necessidades")
        self.tv_fam = ttk.Treeview(self.tab_fam, columns=cols, show="headings")
        for c in cols:
            self.tv_fam.heading(c, text=c)
            self.tv_fam.column(c, width=140)
        self.tv_fam.pack(fill="both", expand=True)

        # botões PDF + Excel
        frame_btn = tk.Frame(self.tab_fam)
        frame_btn.pack(pady=6)

        ttk.Button(frame_btn, text="Exportar PDF",
                   command=lambda: self._exportar_pdf("familias")).grid(row=0, column=0, padx=5)

        ttk.Button(frame_btn, text="Exportar Excel",
                   command=lambda: self._exportar_excel("familias")).grid(row=0, column=1, padx=5)

        self.atualizar_familias()

    # ------------------------------------------------------------------
    # ABA: FREQUÊNCIA
    # ------------------------------------------------------------------
    def _montar_tab_frequencia(self):
        cols = ("ID", "Responsável", "Total Atendimentos")
        self.tv_freq = ttk.Treeview(self.tab_freq, columns=cols, show="headings")
        for c in cols:
            self.tv_freq.heading(c, text=c)
            self.tv_freq.column(c, width=200)
        self.tv_freq.pack(fill="both", expand=True)

        frame_btn = tk.Frame(self.tab_freq)
        frame_btn.pack(pady=6)

        ttk.Button(frame_btn, text="Exportar PDF",
                   command=lambda: self._exportar_pdf("frequencia")).grid(row=0, column=0, padx=5)

        ttk.Button(frame_btn, text="Exportar Excel",
                   command=lambda: self._exportar_excel("frequencia")).grid(row=0, column=1, padx=5)

        self.atualizar_frequencia()

    # ------------------------------------------------------------------
    # ABA: NECESSIDADES
    # ------------------------------------------------------------------
    def _montar_tab_necessidades(self):
        cols = ("Necessidade", "Contagem")
        self.tv_nec = ttk.Treeview(self.tab_nec, columns=cols, show="headings")
        for c in cols:
            self.tv_nec.heading(c, text=c)
            self.tv_nec.column(c, width=200)
        self.tv_nec.pack(fill="both", expand=True)

        frame_btn = tk.Frame(self.tab_nec)
        frame_btn.pack(pady=6)

        ttk.Button(frame_btn, text="Exportar PDF",
                   command=lambda: self._exportar_pdf("necessidades")).grid(row=0, column=0, padx=5)

        ttk.Button(frame_btn, text="Exportar Excel",
                   command=lambda: self._exportar_excel("necessidades")).grid(row=0, column=1, padx=5)

        self.atualizar_necessidades()

    # ------------------------------------------------------------------
    # Atualizações das tabelas
    # ------------------------------------------------------------------
    def atualizar_familias(self):
        for r in self.tv_fam.get_children():
            self.tv_fam.delete(r)
        for row in listar_familias_simples():
            self.tv_fam.insert("", "end", values=row)

    def atualizar_frequencia(self):
        for r in self.tv_freq.get_children():
            self.tv_freq.delete(r)
        for row in frequencia_atendimentos():
            self.tv_freq.insert("", "end", values=row)

    def atualizar_necessidades(self):
        for r in self.tv_nec.get_children():
            self.tv_nec.delete(r)
        for need, count in necessidades_mais_comuns():
            self.tv_nec.insert("", "end", values=(need, count))

    # ------------------------------------------------------------------
    # EXPORTAR PARA PDF
    # ------------------------------------------------------------------
    def _exportar_pdf(self, tipo):
        path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                            filetypes=[("PDF files", "*.pdf")])
        if not path:
            return

        styles = getSampleStyleSheet()
        elems = []
        elems.append(Paragraph("Relatório SFA", styles["Title"]))
        elems.append(Spacer(1, 12))

        if tipo == "familias":
            hdr = ["ID", "Responsável", "Endereço", "Telefone", "Email", "Necessidades"]
            data = [hdr] + [[str(x) if x is not None else "" for x in row]
                            for row in listar_familias_simples()]
        elif tipo == "frequencia":
            hdr = ["ID", "Responsável", "Total Atendimentos"]
            data = [hdr] + [[str(x) for x in row] for row in frequencia_atendimentos()]
        else:
            hdr = ["Necessidade", "Contagem"]
            data = [hdr] + [[n, str(c)] for n, c in necessidades_mais_comuns()]

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d3d3d3")),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))
        elems.append(table)

        doc = SimpleDocTemplate(path, pagesize=A4)

        try:
            doc.build(elems)
            messagebox.showinfo("Exportado", f"PDF salvo em: {path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")

    # ------------------------------------------------------------------
    # EXPORTAR PARA EXCEL (.xlsx)
    # ------------------------------------------------------------------
    def _exportar_excel(self, tipo):
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Arquivo Excel", "*.xlsx")]
        )
        if not path:
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Relatório"

        # Define os dados exportados
        if tipo == "familias":
            hdr = ["ID", "Responsável", "Endereço", "Telefone", "Email", "Necessidades"]
            dados = listar_familias_simples()

        elif tipo == "frequencia":
            hdr = ["ID", "Responsável", "Total Atendimentos"]
            dados = frequencia_atendimentos()

        else:  # necessidades
            hdr = ["Necessidade", "Contagem"]
            dados = necessidades_mais_comuns()

        # Cabeçalho
        ws.append(hdr)

        # Conteúdo
        for linha in dados:
            ws.append(list(linha))

        try:
            wb.save(path)
            messagebox.showinfo("Exportado", f"Excel salvo em:\n{path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar Excel:\n{e}")
