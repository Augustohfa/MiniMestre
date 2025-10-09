import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Dict, Any
from datetime import datetime

from drive_integration import inicializar_drive, limpar_arquivos_locais
from utils import carregar, salvar

ARQ_ALUNOS = "alunos.json"
ARQ_AULAS = "aulas.json"


def calcular_media_e_situacao(aluno: Dict[str, Any]) -> (float, str):
    notas = aluno.get("notas", [])
    faltas = aluno.get("faltas", 0)
    if notas:
        soma_notas = sum(n["valor"] * n["peso"] for n in notas)
        soma_pesos = sum(n["peso"] for n in notas)
        media = soma_notas / soma_pesos if soma_pesos > 0 else 0.0
    else:
        media = 0.0
    situacao = "Aprovado" if media >= 7 and faltas <= 5 else ("Pendente" if not notas else "Reprovado")
    return media, situacao


class LoginFrame(ttk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self._autenticado = False
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="UNIMESTRE", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, pady=(20, 5))
        ttk.Label(
            self,
            text="Autentique-se com o Google Drive e informe a senha do professor para continuar."
        ).grid(row=1, column=0, pady=(0, 15), padx=16)

        self.btn_auth = ttk.Button(self, text="Conectar ao Google Drive", command=self._auth)
        self.btn_auth.grid(row=2, column=0, pady=5)

        self.senha_var = tk.StringVar()
        frm = ttk.Frame(self)
        frm.grid(row=3, column=0, pady=(10, 5))
        ttk.Label(frm, text="Senha do professor:").grid(row=0, column=0, padx=(0, 8))
        self.ent_senha = ttk.Entry(frm, textvariable=self.senha_var, show="*")
        self.ent_senha.grid(row=0, column=1)

        self.btn_entrar = ttk.Button(self, text="Entrar", command=self._entrar, state=tk.DISABLED)
        self.btn_entrar.grid(row=4, column=0, pady=(10, 20))

        self.status = ttk.Label(self, text="Aguardando autenticação...", foreground="#666")
        self.status.grid(row=5, column=0, pady=(0, 10))

    def _auth(self):
        try:
            self.status.config(text="Autenticando com Google Drive...")
            self.update_idletasks()
            inicializar_drive()
            self._autenticado = True
            self.status.config(text="✅ Autenticado com Google Drive")
            self.btn_entrar.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar com Google Drive:\n{e}")
            self.status.config(text="❌ Falha na autenticação")

    def _entrar(self):
        senha_professor = "1234"  # padrão; altere aqui se desejar
        if not self._autenticado:
            messagebox.showwarning("Aviso", "Realize a autenticação com o Google Drive primeiro.")
            return
        if self.senha_var.get() != senha_professor:
            messagebox.showerror("Acesso negado", "Senha incorreta.")
            return
        self.on_success()


class AlunosTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.alunos: List[Dict[str, Any]] = []
        self._build()
        self.reload()

    def _build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(10, 5), padx=10)
        for i in range(6):
            toolbar.columnconfigure(i, weight=0)
        ttk.Button(toolbar, text="Adicionar", command=self.add_aluno).grid(row=0, column=0, padx=2)
        ttk.Button(toolbar, text="Adicionar Nota", command=self.add_nota).grid(row=0, column=1, padx=2)
        ttk.Button(toolbar, text="Remover Nota", command=self.remover_nota).grid(row=0, column=2, padx=2)
        ttk.Button(toolbar, text="Atualizar Faltas", command=self.atualizar_faltas).grid(row=0, column=3, padx=2)
        ttk.Button(toolbar, text="Recarregar", command=self.reload).grid(row=0, column=4, padx=2)
        ttk.Button(toolbar, text="Salvar", command=self.save).grid(row=0, column=5, padx=2)

        cols = ("nome", "notas", "media", "faltas", "situacao")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.tree.heading("nome", text="Nome")
        self.tree.heading("notas", text="Notas (valor x peso)")
        self.tree.heading("media", text="Média")
        self.tree.heading("faltas", text="Faltas")
        self.tree.heading("situacao", text="Situação")
        self.tree.column("nome", width=180)
        self.tree.column("notas", width=260)
        self.tree.column("media", width=70, anchor=tk.E)
        self.tree.column("faltas", width=60, anchor=tk.CENTER)
        self.tree.column("situacao", width=100)

    def reload(self):
        self.alunos = carregar(ARQ_ALUNOS) or []
        self._refresh_table()

    def save(self):
        salvar(ARQ_ALUNOS, self.alunos)
        messagebox.showinfo("Salvar", "Alunos salvos no Google Drive.")

    def _refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, a in enumerate(self.alunos):
            notas = a.get("notas", [])
            notas_str = ", ".join([f"{n['valor']} (peso {n['peso']})" for n in notas]) if notas else "—"
            media, situacao = calcular_media_e_situacao(a)
            self.tree.insert("", tk.END, iid=str(idx),
                             values=(a.get("nome", ""), notas_str, f"{media:.2f}", a.get("faltas", 0), situacao))

    def _get_selected_index(self) -> int:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seleção", "Selecione um aluno na lista.")
            return -1
        return int(sel[0])

    def add_aluno(self):
        nome = simpledialog.askstring("Novo aluno", "Nome do aluno:", parent=self)
        if not nome:
            return
        faltas = simpledialog.askinteger("Faltas", "Número de faltas iniciais (0-999):",
                                         minvalue=0, maxvalue=999, parent=self)
        if faltas is None:
            return
        self.alunos.append({"nome": nome.strip(), "notas": [], "faltas": int(faltas)})
        self._refresh_table()

    def add_nota(self):
        idx = self._get_selected_index()
        if idx < 0:
            return
        valor = simpledialog.askfloat("Nova nota", "Digite a nova nota (0-10):",
                                      minvalue=0.0, maxvalue=10.0, parent=self)
        if valor is None:
            return
        peso = simpledialog.askfloat("Peso", "Digite o peso da nota (ex: 1, 2, 3...):",
                                     minvalue=0.1, parent=self)
        if peso is None:
            return
        self.alunos[idx].setdefault("notas", []).append({"valor": float(valor), "peso": float(peso)})
        self._refresh_table()

    def remover_nota(self):
        idx = self._get_selected_index()
        if idx < 0:
            return
        notas = self.alunos[idx].get("notas", [])
        if not notas:
            messagebox.showinfo("Notas", "Não há notas para remover.")
            return
        opcoes = [f"{i+1}. Nota {n['valor']} (peso {n['peso']})" for i, n in enumerate(notas)]
        escolha = simpledialog.askinteger("Remover nota",
                                          "Digite o número da nota a remover:\n\n" + "\n".join(opcoes),
                                          minvalue=1, maxvalue=len(notas), parent=self)
        if escolha is None:
            return
        notas.pop(escolha - 1)
        self._refresh_table()

    def atualizar_faltas(self):
        idx = self._get_selected_index()
        if idx < 0:
            return
        atual = int(self.alunos[idx].get("faltas", 0))
        novo = simpledialog.askinteger("Atualizar faltas",
                                       f"Novo número de faltas (atual: {atual}):",
                                       minvalue=0, maxvalue=999, parent=self)
        if novo is None:
            return
        self.alunos[idx]["faltas"] = int(novo)
        self._refresh_table()


class AulasTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.aulas: List[Dict[str, Any]] = []
        self._build()
        self.reload()

    def _build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(10, 5), padx=10)
        ttk.Button(toolbar, text="Registrar Aula", command=self.add_aula).grid(row=0, column=0, padx=2)
        ttk.Button(toolbar, text="Recarregar", command=self.reload).grid(row=0, column=1, padx=2)
        ttk.Button(toolbar, text="Salvar", command=self.save).grid(row=0, column=2, padx=2)

        cols = ("data", "conteudo")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.tree.heading("data", text="Data/Hora")
        self.tree.heading("conteudo", text="Conteúdo")
        self.tree.column("data", width=160)
        self.tree.column("conteudo", width=500)

    def reload(self):
        self.aulas = carregar(ARQ_AULAS) or []
        self._refresh_table()

    def save(self):
        salvar(ARQ_AULAS, self.aulas)
        messagebox.showinfo("Salvar", "Aulas salvas no Google Drive.")

    def _refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, a in enumerate(self.aulas):
            self.tree.insert("", tk.END, iid=str(idx), values=(a.get("data", ""), a.get("conteudo", "")))

    def add_aula(self):
        conteudo = simpledialog.askstring("Registro de aula", "Conteúdo da aula:", parent=self)
        if not conteudo:
            return
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.aulas.append({"data": data, "conteudo": conteudo})
        self._refresh_table()


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Unimestre - Sistema Acadêmico")
        self.geometry("860x520")
        self.minsize(760, 420)
        try:
            self.iconbitmap(default="")  # opcional: defina um .ico se desejar
        except Exception:
            pass

        self._login_frame = LoginFrame(self, self._on_login_success)
        self._login_frame.pack(fill="both", expand=True)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_login_success(self):
        self._login_frame.destroy()
        nb = ttk.Notebook(self)
        self._tab_alunos = AlunosTab(nb)
        self._tab_aulas = AulasTab(nb)
        nb.add(self._tab_alunos, text="Alunos")
        nb.add(self._tab_aulas, text="Aulas")
        nb.pack(fill="both", expand=True)

    def _on_close(self):
        try:
            limpar_arquivos_locais()
        finally:
            self.destroy()


def main():
    app = MainApp()
    app.mainloop()


if __name__ == '__main__':
    main()