# screens/alertas.py

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from database.db import get_connection

class AlertasWindow(tk.Toplevel):
    def __init__(self, parent, dias=3):
        super().__init__(parent)
        self.title("Atendimentos Pendentes")
        self.geometry("750x400")
        self.dias_limite = dias

        tk.Label(self, text="Lista de Atendimentos Pendentes", font=("Arial", 16, "bold")).pack(pady=10)

        # Configurar tabela com Treeview
        colunas = ("Família", "Data Atendimento", "Retorno Previsto", "Dias Restantes")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.carregar_alertas()

    def carregar_alertas(self):
        conn = get_connection()
        cursor = conn.cursor()

        # Consulta integrando famílias e atendimentos com join
        cursor.execute("""
            SELECT f.responsavel, a.data, a.retorno_previsto 
            FROM atendimentos a 
            JOIN familias f ON a.id_familia = f.id
            WHERE a.retorno_previsto IS NOT NULL
        """)

        registros = cursor.fetchall()
        conn.close()

        hoje = datetime.now().date()

        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        for responsavel, data_at, data_ret in registros:
            data_at = datetime.strptime(data_at, "%Y-%m-%d").date()
            data_ret = datetime.strptime(data_ret, "%Y-%m-%d").date()

            dias_restantes = (data_ret - hoje).days

            # Adiciona na tabela
            tag = self.definir_cor(dias_restantes)
            
            self.tree.insert(
                "", "end", 
                values=(responsavel, data_at.strftime("%d/%m/%Y"), data_ret.strftime("%d/%m/%Y"), dias_restantes),
                tags=(tag,)
            )

        # Configurar as cores
        self.tree.tag_configure("vermelho", background="#F5B7B1")  # atrasados
        self.tree.tag_configure("amarelo", background="#F9E79F")   # próximos
        self.tree.tag_configure("verde", background="#ABEBC6")     # distantes

    def definir_cor(self, dias_restantes):
        if dias_restantes < 0:
            return "vermelho"  # atrasados
        elif dias_restantes <= self.dias_limite:
            return "amarelo"  # dentro do limite configurado
        else:
            return "verde"    # fora de risco
