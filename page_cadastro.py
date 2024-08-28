import db_requests
from tkinter import ttk, messagebox


class PageCadastro:
    def create_cadastro_tab(self):
        self.cadastro_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cadastro_tab, text="Cadastro")

        ttk.Label(self.cadastro_tab, text="Codigo:").pack(pady=5)
        self.codigo_entry = ttk.Entry(self.cadastro_tab)
        self.codigo_entry.pack(pady=5)

        ttk.Label(self.cadastro_tab, text="Nome:").pack(pady=5)
        self.nome_entry = ttk.Entry(self.cadastro_tab)
        self.nome_entry.pack(pady=5)

        ttk.Label(self.cadastro_tab, text="Senha:").pack(pady=5)
        self.senha_entry = ttk.Entry(self.cadastro_tab, show="*")
        self.senha_entry.pack(pady=5)

        register_button = ttk.Button(
            self.cadastro_tab, text="Cadastrar", command=self.register_polo
        )
        register_button.pack(pady=10)

        columns = ("Código", "Nome", "Senha")
        self.cadastro_tree = ttk.Treeview(
            self.cadastro_tab, columns=columns, show="headings"
        )
        for col in columns:
            self.cadastro_tree.heading(col, text=col.capitalize())
            self.cadastro_tree.column(col, width=120, anchor="center")
        self.cadastro_tree.pack(fill="both", expand=True, pady=10)
        db = db_requests.LocalDB()
        cadastros = db.select_all_for_table("cadastros")
        for cadastro in cadastros:
            self.load_cadastros(*cadastro)
        delete_button = ttk.Button(
            self.cadastro_tab, text="Excluir Polo", command=self.delete_polo
        )
        delete_button.pack(pady=10)

    def load_cadastros(self, cod: str, name: str, password: str):
        self.cadastro_tree.insert("", "end", values=(cod, name, password))

    def register_polo(self):
        codigo = self.codigo_entry.get()
        nome = self.nome_entry.get()
        senha = self.senha_entry.get()
        if codigo and nome and senha:
            TABLE_CADASTRO = "cadastros"
            COLUMNS_CADASTRO = {
                "COD_POLO": f"{codigo}",
                "NOME_POLO": f"{nome}",
                "SENHA": f"{senha}",
            }
            db = db_requests.LocalDB()
            self.codigo_entry.delete(0, "end")
            self.nome_entry.delete(0, "end")
            self.senha_entry.delete(0, "end")
            db.insert_table(TABLE_CADASTRO, COLUMNS_CADASTRO)
            self.load_cadastros(codigo, nome, senha)
            messagebox.showinfo("Polo Cadastrado", "O polo foi cadastrado com sucesso!")
        else:
            messagebox.showwarning("Aviso!", f"Preencha todos os campos!")

    def delete_polo(self):
        selected_item = self.cadastro_tree.selection()
        if selected_item:
            item_data = self.cadastro_tree.item(selected_item)
            values: str = item_data["values"]
            print(f"Dados selecionados para exclusão: {values}")
            confirm = messagebox.askyesno(
                "Confirmação",
                f"Tem certeza que deseja excluir o polo {values[1].capitalize()}?",
            )

            if confirm:
                db = db_requests.LocalDB()
                db.delete_in_table("cadastros", "COD_POLO", values[0])
                self.cadastro_tree.delete(selected_item)
        else:
            messagebox.showwarning(
                "Aviso!", f"Escolha qual polo deseja excluir primeiro!"
            )


if __name__ == "__main__":
    ...
