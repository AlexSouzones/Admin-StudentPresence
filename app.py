import tkinter as tk
from tkinter import ttk
from page_atividades import PageAtividades
from page_carregamento import PageCarregamento
from page_cadastro import PageCadastro


class App(tk.Tk, PageAtividades, PageCarregamento, PageCadastro):
    def __init__(self):
        super().__init__()
        self.title("Gestão de Atividades")
        self.geometry("800x600")
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Helvetica", 14))
        self.style.configure("Treeview", font=("Helvetica", 12))
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        self.excel_instance = None
        self.create_atividades_tab()
        self.create_carregamento_tab()
        self.create_cadastro_tab()


if __name__ == "__main__":
    app = App()
    app.mainloop()
