progress_status = {"valor": 0}


def atualizar_progresso(valor):
    progress_status["valor"] = valor


def obter_progresso():
    return progress_status
