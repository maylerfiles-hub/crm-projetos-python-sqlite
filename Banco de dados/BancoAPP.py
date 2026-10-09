import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import sqlite3  
import json
import os

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class BancoDados:
    
    def __init__(self, nome_banco="crm_projetos.db"):
        self.nome_banco = nome_banco
        self.conexao = sqlite3.connect(self.nome_banco)
        self.criar_tabela()

    def criar_tabela(self):
        cursor = self.conexao.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projetos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                stack TEXT NOT NULL,
                valor REAL NOT NULL
            )
        ''')
        self.conexao.commit()

    def inserir(self, nome, stack, valor):
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO projetos (nome, stack, valor) VALUES (?, ?, ?)",
            (nome, stack, float(valor))
        )
        self.conexao.commit()
            
    def listar_dados(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id, nome, stack, valor FROM projetos ORDER BY id DESC")
        return cursor.fetchall()
    
    def excluir(self, id_projetos):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM projetos WHERE id = ?", (id_projetos,))
        self.conexao.commit()
       
    def fechar(self):
        self.conexao.close()


class JanelaDetalhes(ctk.CTkToplevel):

    def __init__(self, parent, dados_projeto):
        super().__init__(parent)
        self.title(f"Auditoria - ID: {dados_projeto[0]}")
        self.geometry("400x250")
        self.resizable(False, False)
        self.lift()
        self.attributes("-topmost", True)
        
        # CORRIGIDO: É necessário chamar a função para renderizar os elementos na tela
        self._criar_widgets(dados_projeto)

    def _criar_widgets(self, dados):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(frame, text="Detalhamento Técnico do Projeto", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(frame, text=f"ID do Registro: {dados[0]}", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(frame, text=f"Projeto/Cliente: {dados[1]}", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(frame, text=f"Stack Tecnológica: {dados[2]}", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20, pady=2)
        
        # Formatando o valor para float com segurança antes de exibir
        valor_formatado = float(dados[3])
        ctk.CTkLabel(frame, text=f"Orçamento Alocado: R$ {valor_formatado:.2f}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#108981").pack(anchor="w", padx=20, pady=6)

        ctk.CTkButton(frame, text="Fechar", command=self.destroy, fg_color="#EF4444", hover_color="#DC2626").pack(pady=15)

    
class DashboardApp(ctk.CTk):  # CORRIGIDO: Sintaxe da herança ajustada de (ctk,CTk) para (ctk.CTk)
        
    def __init__(self):  # CORRIGIDO: Corrigido de 'sef' para 'self'
        super().__init__()  # CORRIGIDO: Corrigido de '_init_' para '__init__'
        self.title("Sistema de Gestão de Projetos - POO + SQlite + TTK")
        self.geometry("900x550")
        self.minsize(850, 500)

        self.db = BancoDados()

        # CORRIGIDO: O método abaixo chamava _configurar_estilo_ttk, mas o nome real era no plural
        self._configurar_estilos_ttk()
        self._construir_interface()
        self._atualizar_tabela_ui()

    def _configurar_estilos_ttk(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             font=("Arial", 11),
                             rowheight=28,
                             background="#F3F4F6",
                             fieldbackground="#F3F4F6",
                             foreground="#1F2937")
        self.style.configure("Treeview.Heading",
                             font=("Arial", 11, "bold"),
                             background="#E5E7EB",
                             foreground="#1F2637",
                             relief="flat")
        self.style.map("Treeview", background=[("selected", "#2563EB")], foreground=[("selected", "#FFFFFF")])

    # CORRIGIDO: Daqui para baixo, todas as funções foram movidas para DENTRO da classe DashboardApp (Indentação)
    def _construir_interface(self):
        self.tabview = ctk.CTkTabview(self, width=860, height=520)
        self.tabview.pack(padx=15, pady=15, fill="both", expand=True)

        self.tab_geral = self.tabview.add("Painel Geral e CRUD")
        self.tab_config = self.tabview.add("Configurações do Sistema")

        self._renderizar_aba_geral()
        self._renderizar_aba_config()

    def _renderizar_aba_geral(self):
        # Frame de Formulário (Esquerda)
        frame_form = ctk.CTkFrame(self.tab_geral, width=280, corner_radius=10)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Cadastrar Projeto", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        ctk.CTkLabel(frame_form, text="Nome do Projeto:").pack(anchor="w", padx=15)
        self.entry_nome = ctk.CTkEntry(frame_form, placeholder_text="Ex: Sistema de Vendas", width=220)
        self.entry_nome.pack(pady=(0, 10), padx=15)

        ctk.CTkLabel(frame_form, text="Stack Tecnológica:").pack(anchor="w", padx=15)
        self.entry_stack = ctk.CTkEntry(frame_form, placeholder_text="Ex: Python, SQLite", width=220)
        self.entry_stack.pack(pady=(0, 10), padx=15)

        ctk.CTkLabel(frame_form, text="Orçamento (R$):").pack(anchor="w", padx=15)
        self.entry_valor = ctk.CTkEntry(frame_form, placeholder_text="Ex: 4500", width=220)
        self.entry_valor.pack(pady=(0, 20), padx=15)

        ctk.CTkButton(frame_form, text="Salvar no Banco (INSERT)", command=self._cadastrar_projeto, fg_color="#10B981", hover_color="#059669").pack(pady=5, padx=15, fill="x")
        ctk.CTkButton(frame_form, text="Limpar Campos", command=self._limpar_campos, fg_color="transparent", border_width=1, text_color=("#1F2937", "#F9FAFB")).pack(pady=5, padx=15, fill="x")

        # Frame da Tabela e Operações (Direita)
        frame_tabela = ctk.CTkFrame(self.tab_geral, corner_radius=10)
        frame_tabela.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        colunas = ("id", "projeto", "stack", "valor")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("projeto", text="Projeto / Cliente")
        self.tree.heading("stack", text="Tecnologias")
        self.tree.heading("valor", text="Orçamento (R$)")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("projeto", width=180, anchor="w")
        self.tree.column("stack", width=150, anchor="w")
        self.tree.column("valor", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Painel Inferior de Botões de Ação
        frame_acoes = ctk.CTkFrame(frame_tabela, fg_color="transparent")
        frame_acoes.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(frame_acoes, text="Auditar (Detalhes)", fg_color="#3B82F6", hover_color="#2563EB", command=self._abrir_detalhes).pack(side="left", padx=5)
        ctk.CTkButton(frame_acoes, text="Excluir Registro (DELETE)", fg_color="#EF4444", hover_color="#DC2626", command=self._deletar_projeto).pack(side="left", padx=5)
        ctk.CTkButton(frame_acoes, text="Exportar JSON", fg_color="#F59E0B", hover_color="#D97706", command=self._exportar_json).pack(side="right", padx=5)

    def _renderizar_aba_config(self):
        frame_config = ctk.CTkFrame(self.tab_config, corner_radius=10)
        frame_config.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_config, text="Parâmetros de Interface Visual", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15, padx=20, anchor="w")
        
        self.switch_var = ctk.StringVar(value="dark" if ctk.get_appearance_mode() == "Dark" else "light")
        self.switch_tema = ctk.CTkSwitch(
            frame_config,
            text="Alternar Modo Escuro (Afeta Tabela TTK e Controles CTK)",
            command=self._alternar_tema,
            variable=self.switch_var,
            onvalue="dark",
            offvalue="light"
        )
        self.switch_tema.pack(pady=10, padx=20, anchor="w")

    def _atualizar_tabela_ui(self):
        """Lê os dados em tempo real do banco SQLite e atualiza o Treeview."""
        self.tree.delete(*self.tree.get_children())
        # CORRIGIDO: O método correto na classe BancoDados é 'listar_dados'
        registros = self.db.listar_dados()
        for item in registros:
            self.tree.insert("", "end", values=item)

    def _cadastrar_projeto(self):
        nome = self.entry_nome.get().strip()
        stack = self.entry_stack.get().strip()
        valor_str = self.entry_valor.get().strip()

        if not nome or not stack or not valor_str:
            messagebox.showwarning("Aviso de Validação", "Preencha todos os campos do formulário.")
            return

        try:
            valor = float(valor_str)
        except ValueError:
            messagebox.showerror("Erro de Formatação", "O campo de Orçamento deve conter apenas números (ex: 1500 ou 1500.50).")
            return

        # Persiste no banco de dados e recarrega a UI
        self.db.inserir(nome, stack, valor)
        self._atualizar_tabela_ui()  # CORRIGIDO: Nome do método corrigido aqui
        self._limpar_campos()
        messagebox.showinfo("Sucesso", "Projeto gravado com sucesso no banco de dados SQLite!")

    def _deletar_projeto(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma linha da tabela para excluir.")
            return

        id_projeto = self.tree.item(selecionado[0], "values")[0]
        confirmacao = messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente remover o registro ID {id_projeto} do banco de dados?")

        if confirmacao:
            self.db.excluir(id_projeto)
            self._atualizar_tabela_ui()

    def _abrir_detalhes(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma linha da tabela para auditar.")
            return

        dados_linha = self.tree.item(selecionado[0], "values")
        JanelaDetalhes(self, dados_linha)

    def _exportar_json(self):
        caminho = filedialog.asksaveasfilename(
            title="Exportar Relatório do Banco de Dados",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json")]
        )

        if not caminho:
            return

        # CORRIGIDO: Nome do método corrigido para listar_dados
        registros = self.db.listar_dados()
        dados_exportacao = []
        for reg in registros:
            dados_exportacao.append({
                "id": reg[0],
                "projeto": reg[1],
                "tecnologia": reg[2],
                "orcamento": float(reg[3])
            })

        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados_exportacao, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Exportação Concluída", f"Arquivo gerado com sucesso em:\n{os.path.basename(caminho)}")
        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Falha ao gerar o arquivo JSON: {str(e)}")

    def _limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_stack.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)

    def _alternar_tema(self):
        modo = self.switch_var.get()
        if modo == "dark":
            ctk.set_appearance_mode("Dark")
            self.style.configure("Treeview", background="#1F2937", fieldbackground="#1F2937", foreground="#F3F4F6")
            self.style.configure("Treeview.Heading", background="#374151", foreground="#F3F4F6")
        else:
            ctk.set_appearance_mode("Light")
            self.style.configure("Treeview", background="#F3F4F6", fieldbackground="#F3F4F6", foreground="#1F2937")
            self.style.configure("Treeview.Heading", background="#E5E7EB", foreground="#1F2937")

    def destroy(self):
        """Sobrescreve o fechamento da janela para encerrar a conexão com o banco de forma segura."""
        self.db.fechar()
        super().destroy()


if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()