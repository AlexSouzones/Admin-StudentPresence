import db_requests
from tkinter import ttk, messagebox


class PageAtividades:
    def load_activity(self):
        self.atividades_tree.delete(*self.atividades_tree.get_children())
        db = db_requests.LocalDB()
        self.atividades = db.load_table("atividades")
        for atividade in self.atividades:
            self.add_activity(*atividade)

    def create_atividades_tab(self):
        self.atividades_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.atividades_tab, text="Atividades")

        scrollbar = ttk.Scrollbar(self.atividades_tab)
        scrollbar.pack(side="right", fill="y")

        columns = ("status", "disciplina", "data", "hora", "download")
        self.atividades_tree = ttk.Treeview(
            self.atividades_tab,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        self.atividades_tree.pack(fill="both", expand=True)

        scrollbar.config(command=self.atividades_tree.yview)

        for col in columns:
            self.atividades_tree.heading(col, text=col.capitalize())
            self.atividades_tree.column(col, width=120, anchor="center")

        self.load_activity()
        delete_button = ttk.Button(
            self.atividades_tab, text="Excluir Atividade", command=self.delete_activity
        )
        delete_button.pack(pady=10)

    def add_activity(
        self, code: str, disciplina: str, data: str, hora: str, status: str
    ):
        if status == "encerrado":
            self.atividades_tree.insert(
                "", "end", id=code, values=(status, disciplina, data, hora, "Download")
            )
        else:
            self.atividades_tree.insert(
                "", "end", id=code, values=(status, disciplina, data, hora, "-")
            )

    def delete_activity(self):
        selected_item = self.atividades_tree.selection()
        if selected_item:
            item_data = self.atividades_tree.item(selected_item)
            values: str = item_data["values"]
            confirm = messagebox.askyesno(
                "Confirmação",
                f"Tem certeza que deseja excluir a atividade referente a disciplina {values[1].capitalize()}?",
            )

            if confirm:
                db = db_requests.LocalDB()
                db.delete_in_table("atividades", "COD_ATIVIDADE", selected_item[0])
                self.atividades_tree.delete(selected_item)
        else:
            messagebox.showwarning(
                "Aviso!", f"Escolha qual atividade deseja excluir primeiro!"
            )


if __name__ == "__main__":
    ...
