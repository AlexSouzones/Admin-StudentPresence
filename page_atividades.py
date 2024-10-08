import db_requests
from tkinter import ttk, messagebox
from planilha import planilha_insert
from utils import verificar_data, verificar_horario


class PageAtividades:
    def load_activity(self):
        self.atividades_tree.delete(*self.atividades_tree.get_children())
        db = db_requests.LocalDB()
        self.atividades = db.load_table("atividades")
        for atividade in self.atividades:
            status_data = verificar_data(atividade[2])
            if status_data == "Em Andamento":
                if verificar_horario(atividade[3]):
                    self.add_activity(*atividade, "Em Andamento")
                    continue
                else:
                    self.add_activity(*atividade, "Aguardando")
                    continue
            self.add_activity(*atividade, status_data)
            

    def create_atividades_tab(self):
        self.atividades_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.atividades_tab, text="Atividades")

        scrollbar = ttk.Scrollbar(self.atividades_tab)
        scrollbar.pack(side="right", fill="y")

        columns = ("status", "disciplina", "data", "hora")
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
        download_button = ttk.Button(
            self.atividades_tab, text="Baixar Atividade", command=self.download_activity
        )
        download_button.pack(pady=10)

    def add_activity(
        self, code: str, disciplina: str, data: str, hora: str, status: str
    ):
        self.atividades_tree.insert(
            "", "end", id=code, values=(status, disciplina, data, hora)
        )
    
    def download_activity(self):
        selected_item = self.atividades_tree.selection()
        if selected_item:
            item_data = self.atividades_tree.item(selected_item)
            values: str = item_data["values"]
            if values[0] == "Encerrado":
                db = db_requests.LocalDB()
                info = db.select_table("alunos", "COD_ATIVIDADE", selected_item[0])
                planilha_insert(info, values[1])
                messagebox.showinfo(
                    "Concluído!", f"A planilha foi gerada com sucesso!"
                )
            else:
                messagebox.showwarning(
                "Aviso!", f"A atividade ainda não foi encerrada!"
            )
        else:
            messagebox.showwarning(
                "Aviso!", f"Escolha qual atividade deseja baixar primeiro!"
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
                db.delete_in_table("polos", "COD_ATIVIDADE", selected_item[0])
                db.delete_in_table("alunos", "COD_ATIVIDADE", selected_item[0])
                db.delete_in_table("atividades", "COD_ATIVIDADE", selected_item[0])
                self.atividades_tree.delete(selected_item)
        else:
            messagebox.showwarning(
                "Aviso!", f"Escolha qual atividade deseja excluir primeiro!"
            )


if __name__ == "__main__":
    ...
