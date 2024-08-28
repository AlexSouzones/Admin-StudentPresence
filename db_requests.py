import sqlite3
from pathlib import Path
import uuid


class LocalDB:
    def __init__(self):
        ROOT_DIR = Path(__file__).parent
        DB_NAME = "db.sqlite3"
        self.DB_FILE = ROOT_DIR / DB_NAME
        self.connection = None
        self.cursor = None

    def __open_connection(self) -> None:
        self.connection = sqlite3.connect(self.DB_FILE)
        self.cursor = self.connection.cursor()

    def __close_connection(self) -> None:
        self.cursor.close()
        self.connection.close()

    def create_table(self, table_name: str, columns: dict[str]) -> None:
        column_defs = ", ".join(f"{key} {value}" for key, value in columns.items())
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"

        self.__open_connection()
        self.cursor.execute(create_table_sql)
        self.connection.commit()
        self.__close_connection()

    def insert_table(self, table_name: str, columns_values: dict[str]) -> None:
        columns = ", ".join(columns_values.keys())
        placeholders = ", ".join("?" for _ in columns_values)
        values = tuple(columns_values.values())

        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        self.__open_connection()
        self.cursor.execute(insert_sql, values)
        self.connection.commit()
        self.__close_connection()

    def select_table(
        self, table_name: str, column: str, value: str
    ) -> list[tuple[str]]:
        insert_sql = f"select * from {table_name} WHERE {column} = {value}"
        self.__open_connection()
        self.cursor.execute(insert_sql)
        result = self.cursor.fetchall()
        self.__close_connection()
        return result

    def select_all_for_table(self, table_name: str) -> list[tuple[str]]:
        insert_sql = f"select * from {table_name}"
        self.__open_connection()
        self.cursor.execute(insert_sql)
        result = self.cursor.fetchall()
        self.__close_connection()
        return result

    def load_table(self, table_name: str) -> list[tuple[str]]:
        insert_sql = f"select * from {table_name}"
        self.__open_connection()
        self.cursor.execute(insert_sql)
        result = self.cursor.fetchall()
        self.__close_connection()
        return result

    def delete_in_table(self, table_name: str, column: str, condition: str) -> None:
        sql_command = f"delete from {table_name} WHERE {column} = '{condition}'"
        self.__open_connection()
        self.cursor.execute(sql_command)
        self.connection.commit()
        self.__close_connection()

    def insert_big_data(self, table_name: str, sql_code: str, valores: tuple):
        self.__open_connection()
        self.cursor.executemany(f"{sql_code}", valores)
        self.connection.commit()
        self.__close_connection()

    def unique_key(self, table_name: str, column: str):
        while True:
            new_key = str(uuid.uuid4())
            self.__open_connection()
            self.cursor.execute(
                f"SELECT * FROM {table_name} WHERE `{column}` = '{new_key}'"
            )
            if not self.cursor.fetchall():
                self.__close_connection()
                return new_key
            self.__close_connection()


if __name__ == "__main__":
    TABLE_ALUNOS = "alunos"
    COLUMNS_ALUNOS = {
        "COD_POLO": "TEXT",
        "POLO_EAD": "TEXT",
        "RA": "TEXT",
        "ALUNO": "TEXT",
        "CURSO": "TEXT",
        "DISCIPLINA": "TEXT",
        "COD_ATIVIDADE": "TEXT",
        "Presente": "TEXT",
    }

    TABLE_ATIVIDADE = "atividades"
    COLUMNS_ATIVIDADE = {
        "COD_ATIVIDADE": "TEXT PRIMARY KEY",
        "DISCIPLINA": "TEXT",
        "DATA": "DATE",
        "HORA": "TIME",
        "STATUS": "TEXT",
    }

    TABLE_POLO = "polos"
    COLUMNS_POLO = {"COD_POLO": "TEXT", "POLO_EAD": "TEXT", "COD_ATIVIDADE": "TEXT"}

    TABLE_CADASTRO = "cadastros"
    COLUMNS_CADASTRO = {
        "COD_POLO": "TEXT PRIMARY KEY",
        "NOME_POLO": "TEXT",
        "SENHA": "TEXT",
    }
    db = LocalDB()
    db.create_table(TABLE_ALUNOS, COLUMNS_ALUNOS)
    db.create_table(TABLE_ATIVIDADE, COLUMNS_ATIVIDADE)
    db.create_table(TABLE_POLO, COLUMNS_POLO)
    db.create_table(TABLE_CADASTRO, COLUMNS_CADASTRO)
    print(db.load_table(TABLE_ALUNOS))
    print(db.unique_key(TABLE_ATIVIDADE, "COD_ATIVIDADE"))
