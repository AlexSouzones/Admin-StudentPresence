import db_requests
from tkinter import ttk, filedialog, messagebox
from planilha import PlanilhaManager
from utils import verificar_formato_data, verificar_formato_horario


class PageCarregamento:
    def create_carregamento_tab(self):
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TEntry", font=("Arial", 12), padding=5)
        self.carregamento_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.carregamento_tab, text="Carregamento")
        upload_button = ttk.Button(
            self.carregamento_tab,
            text="Selecionar Planilha",
            command=self.upload_spreadsheet,
        )
        upload_button.pack(pady=5)

        self.data_entry = ttk.Entry(self.carregamento_tab)
        self.hora_entry = ttk.Entry(self.carregamento_tab)

        columns = ("Cod Polo", "Polo", "Total de Alunos")
        column_info = {"Cod Polo": 20, "Polo": 260, "Total de Alunos": 80}
        self.carregamento_tree = ttk.Treeview(
            self.carregamento_tab,
            columns=columns,
            show="headings",
            selectmode="none",
        )

        for col in columns:
            self.carregamento_tree.heading(col, text=col.capitalize())
            self.carregamento_tree.column(col, width=column_info[col], anchor="center")

        self.subir_dados_button = ttk.Button(
            self.carregamento_tab,
            text="Subir Dados",
            state="normal",
            command=self.upload_data,
        )

    def add_activits(self, polos: list[dict]):
        for dictionary in polos:
            self.carregamento_tree.insert(
                "",
                "end",
                values=(
                    dictionary["COD POLO"],
                    dictionary["Polo"],
                    len(dictionary["Alunos"]),
                ),
            )

    def upload_spreadsheet(self):
        try:
            try:
                self.file_path = None
                self.carregamento_tree.delete(*self.carregamento_tree.get_children())
                self.data_entry.delete(0, "end")
                self.hora_entry.delete(0, "end")
                self.subir_dados_button.delete(0, "end")
                self.carregamento_tree.delete()
            except:
                ...
            self.file_path = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx")]
            )
            self.excel_instance = PlanilhaManager(self.file_path)
            self.excel_instance.loading()
            self.add_activits(self.excel_instance.info)
            if self.file_path:
                self.data_entry.pack(pady=5)
                self.data_entry.insert(0, "DD/MM/AAAA")
                self.hora_entry.pack(pady=5)
                self.hora_entry.insert(0, "HH:MM")
                self.carregamento_tree.pack(fill="both", expand=True, pady=10)
                self.subir_dados_button.pack(pady=10)
        except Exception as erro:
            messagebox.showerror(
                "Planilha Inválida",
                f"A planilha não foi inserida ou contém colunas inválidas! {erro}",
            )

    def upload_data(self):
        data = self.data_entry.get()
        hora = self.hora_entry.get()
        if verificar_formato_horario(hora) and verificar_formato_data(data):
            try:
                db = db_requests.LocalDB()
                cod_atividade = db.unique_key("atividades", "COD_ATIVIDADE")

                sql_polo = """INSERT INTO polos (COD_POLO, POLO_EAD, COD_ATIVIDADE)
            VALUES (?, ?, ?)"""
                sql_aluno = """INSERT INTO alunos (COD_POLO, POLO_EAD, RA, ALUNO, CURSO, DISCIPLINA, COD_ATIVIDADE, Presente)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                TABLE_ATIVIDADE = "atividades"
                COLUMNS_ATIVIDADE = {
                    "COD_ATIVIDADE": f"{cod_atividade}",
                    "DISCIPLINA": self.excel_instance.disciplina,
                    "DATA": f"{data}",
                    "HORA": f"{hora}",
                }
                TABLE_POLO = "polos"

                db.insert_table(TABLE_ATIVIDADE, COLUMNS_ATIVIDADE)
                lista_polo = [
                    (polo["COD POLO"], polo["Polo"], cod_atividade)
                    for polo in self.excel_instance.info
                ]
                db.insert_big_data(TABLE_POLO, sql_polo, lista_polo)
                for polo in self.excel_instance.info:
                    cod_polo = polo["COD POLO"]
                    polo_ead = polo["Polo"]

                    lista_alunos = [
                        (
                            cod_polo,
                            polo_ead,
                            aluno["matricula"],
                            aluno["nome"],
                            aluno["Curso"],
                            aluno["Disciplina"],
                            cod_atividade,
                            "Aguardando",
                        )
                        for aluno in polo["Alunos"]
                    ]
                    db.insert_big_data("alunos", sql_aluno, lista_alunos)
                self.load_activity()
                try:
                    self.file_path = None
                    self.carregamento_tree.delete(
                        *self.carregamento_tree.get_children()
                    )
                    self.carregamento_tree.delete()
                    self.data_entry.delete(0, "end")
                    self.hora_entry.delete(0, "end")
                    self.subir_dados_button.delete(0, "end")
                except:
                    ...
                messagebox.showinfo("Dados Upados", "A atividade foi registrada!")
            except Exception as erro:
                messagebox.showerror(
                    "Dados Não Upados",
                    f"Aconteceu algum problema ao tentar subir os dados para o banco!\n{erro}",
                )
        else:
            messagebox.showwarning(
                "Atenção!",
                "Data ou Hora não seguem o padrão estabelecido!\nData: 'DD/MM/AAAA'\nHora: 'HH:MM' (Padrão 24h e não 12h)",
            )


if __name__ == "__main__":
    ...
