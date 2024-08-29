from datetime import datetime


def verificar_formato_data(data_input: str) -> bool:
    try:
        datetime.strptime(data_input, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def verificar_formato_horario(horario_input: str) -> bool:
    try:
        datetime.strptime(horario_input, "%H:%M")
        return True
    except ValueError:
        return False


def verificar_horario(horario_input: str) -> bool:
    horario_formatado = datetime.strptime(horario_input, "%H:%M").time()
    horario_atual = datetime.now().time()

    if horario_formatado < horario_atual:
        return True
    else:
        return False


def verificar_data(data_input: str) -> str:
    data_formatada = datetime.strptime(data_input, "%d/%m/%Y").date()
    data_atual = datetime.today().date()

    if data_formatada < data_atual:
        return "Aguardando"
    elif data_formatada > data_atual:
        return "Encerrado"
    else:
        return "Em Andamento"


if __name__ == "__main__":
    ...
