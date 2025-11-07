# screens/atendimentos.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from database.db import get_connection
from services.familia_service import listar_familias


def abrir_atendimento(master, usuario_logado):
    janela = tk.Toplevel(master)
    janela.title("Registro de Atendimentos")
    janela.geometry("750x600")

    tk.Label(janela, text="Registro de Atendimentos", font=("Arial", 16, "bold")).pack(pady=10)

    # =========================
    # CAMPOS DO FORMULÁRIO
    # =========================
    frame_form = tk.Frame(janela)
    frame_form.pack(padx=15, pady=10, fill="x")

    # Família atendida
    tk.Label(frame_form, text="Família atendida:").grid(row=0, column=0, sticky="w")
    combo_familia = ttk.Combobox(frame_form, state="readonly", width=40)
    combo_familia.grid(row=0, column=1, padx=5, pady=5)

    familias = listar_familias()
    combo_familia["values"] = [f"{f.id} - {f.responsavel}" for f in familias]

    # Data do atendimento
    tk.Label(frame_form, text="Data do atendimento:").grid(row=1, column=0, sticky="w")
    entry_data = DateEntry(frame_form, date_pattern="dd/mm/yyyy", width=12)
    entry_data.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    # Tipo de auxílio
    tk.Label(frame_form, text="Tipo de auxílio:").grid(row=2, column=0, sticky="w")
    combo_auxilio = ttk.Combobox(
        frame_form,
        values=["Cesta básica", "Consulta médica", "Apoio psicológico", "Orientação jurídica", "Outros"],
        state="readonly",
        width=37
    )
    combo_auxilio.grid(row=2, column=1, padx=5, pady=5)

    # Responsável (usuário logado)
    tk.Label(frame_form, text="Responsável pelo atendimento:").grid(row=3, column=0, sticky="w")
    entry_responsavel = tk.Entry(frame_form, width=40)
    entry_responsavel.insert(0, usuario_logado.nome)
    entry_responsavel.config(state="disabled")
    entry_responsavel.grid(row=3, column=1, padx=5, pady=5)

    # Observações
    tk.Label(frame_form, text="Observações:").grid(row=4, column=0, sticky="nw")
    entry_observacoes = tk.Text(frame_form, width=45, height=4)
    entry_observacoes.grid(row=4, column=1, padx=5, pady=5)

    # Retorno previsto
    tk.Label(frame_form, text="Data prevista para retorno:").grid(row=5, column=0, sticky="w")
    entry_retorno = DateEntry(frame_form, date_pattern="dd/mm/yyyy", width=12)
    entry_retorno.grid(row=5, column=1, sticky="w", padx=5, pady=5)

    # =========================
    # TABELA DE ATENDIMENTOS
    # =========================
    tk.Label(janela, text="Atendimentos Registrados", font=("Arial", 12, "bold")).pack(pady=(10, 0))

    colunas = ("ID", "Família", "Data", "Tipo", "Responsável", "Retorno", "Observações")
    tree = ttk.Treeview(janela, columns=colunas, show="headings", height=10)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Função para carregar atendimentos
    def carregar_atendimentos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, f.responsavel, a.data, a.tipo_auxilio, u.nome, a.retorno_previsto, a.observacoes
            FROM atendimentos a
            JOIN familias f ON a.id_familia = f.id
            JOIN usuarios u ON a.id_usuario = u.id
            ORDER BY a.data DESC
        """)
        dados = cursor.fetchall()
        conn.close()

        for i in tree.get_children():
            tree.delete(i)
        for linha in dados:
            tree.insert("", "end", values=linha)

    carregar_atendimentos()

    # =========================
    # FUNÇÕES DE CRUD
    # =========================
    def salvar_atendimento():
        if not combo_familia.get() or not combo_auxilio.get():
            messagebox.showwarning("Aviso", "Preencha os campos obrigatórios.")
            return

        id_familia = combo_familia.get().split(" - ")[0]
        data_at = datetime.strptime(entry_data.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        tipo_auxilio = combo_auxilio.get()
        observacoes = entry_observacoes.get("1.0", tk.END).strip()
        retorno = datetime.strptime(entry_retorno.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        id_usuario = usuario_logado.id

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO atendimentos (id_familia, data, tipo_auxilio, observacoes, retorno_previsto, id_usuario)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id_familia, data_at, tipo_auxilio, observacoes, retorno, id_usuario))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Atendimento salvo com sucesso!")
            carregar_atendimentos()

            combo_familia.set("")
            combo_auxilio.set("")
            entry_observacoes.delete("1.0", tk.END)
            entry_data.set_date(datetime.today())
            entry_retorno.set_date(datetime.today())

        except Exception as e:
            messagebox.showerror("Erro ao salvar", f"Ocorreu um erro:\n{str(e)}")

    def editar_atendimento():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um atendimento para editar.")
            return

        item = tree.item(selecionado[0])
        id_atendimento = item["values"][0]

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT a.id_familia, a.data, a.tipo_auxilio, a.observacoes, a.retorno_previsto
                FROM atendimentos a
                WHERE a.id = ?
            """, (id_atendimento,))
            registro = cursor.fetchone()

            if registro:
                id_familia, data, tipo, obs, retorno = registro
                combo_familia.set(f"{id_familia} - (editando)")
                entry_data.set_date(datetime.strptime(data, "%Y-%m-%d"))
                combo_auxilio.set(tipo)
                entry_observacoes.delete("1.0", tk.END)
                entry_observacoes.insert("1.0", obs)
                entry_retorno.set_date(datetime.strptime(retorno, "%Y-%m-%d"))

                # Confirma atualização
                if messagebox.askyesno("Confirmar edição", "Deseja salvar as alterações?"):
                    cursor.execute("""
                        UPDATE atendimentos
                        SET tipo_auxilio=?, observacoes=?, retorno_previsto=?
                        WHERE id=?
                    """, (combo_auxilio.get(), entry_observacoes.get("1.0", tk.END).strip(),
                          datetime.strptime(entry_retorno.get(), "%d/%m/%Y").strftime("%Y-%m-%d"),
                          id_atendimento))
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Atendimento atualizado com sucesso!")

            conn.close()
            carregar_atendimentos()

        except Exception as e:
            messagebox.showerror("Erro ao editar", f"Ocorreu um erro:\n{str(e)}")

    def excluir_atendimento():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um atendimento para excluir.")
            return

        item = tree.item(selecionado[0])
        id_atendimento = item["values"][0]

        if not messagebox.askyesno("Confirmar exclusão", "Tem certeza que deseja excluir este atendimento?"):
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM atendimentos WHERE id = ?", (id_atendimento,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Atendimento excluído com sucesso!")
            carregar_atendimentos()

        except Exception as e:
            messagebox.showerror("Erro ao excluir", f"Ocorreu um erro:\n{str(e)}")

    # =========================
    # BOTÕES
    # =========================
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Salvar", command=salvar_atendimento, bg="#27AE60", fg="white", width=15).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Editar", command=editar_atendimento, bg="#F1C40F", fg="black", width=15).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Excluir", command=excluir_atendimento, bg="#C0392B", fg="white", width=15).pack(side="left", padx=5)

    janela.mainloop()
