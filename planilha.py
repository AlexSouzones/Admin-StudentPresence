import pandas as pd


class PlanilhaManager:
    def __init__(self, file: str) -> None:
        self.file = file
        self.disciplina: str = None
        self.polos: list[str] = []
        self.info: list[dict[str, list[dict[str]]]] = []

    def polo_content(self, polo_argument: str) -> bool:
        for dictionary in self.info:
            if polo_argument == dictionary["Polo"]:
                return True
        return False

    def insert_into_polo(self, polo: str, info_data: dict[str]):
        for dictionary in self.info:
            if polo == dictionary["Polo"]:
                dictionary["Alunos"].append(info_data)

    def get_disciplina(self) -> str:
        try:
            self.disciplina = self.info[0]["Disciplina"]
            return self.disciplina
        except:
            return False

    def loading(self):
        df = pd.read_excel(self.file)
        for index, row in df.iterrows():
            if not self.disciplina:
                self.disciplina = row["DISCIPLINA"]
            polo = row["POLO EAD"]
            cod = row["COD POLO"]
            info_aluno = {
                "matricula": f"{row['RA']}",
                "nome": f"{row['ALUNO']}",
                "Curso": f"{row['CURSO']}",
                "Disciplina": f"{self.disciplina}",
            }
            if not self.polo_content(polo):
                self.info.append(
                    {
                        "COD POLO": f"{cod}",
                        "Polo": f"{polo}",
                        "Alunos": [info_aluno],
                    }
                )
            else:
                self.insert_into_polo(polo, info_aluno)


if __name__ == "__main__":
    ...
