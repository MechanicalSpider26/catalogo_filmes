# validacoes.py

def validar_diretor(nome, nacionalidade, data_nascimento):
    """Valida os dados de cadastro e edição do diretor."""
    nome = str(nome).strip() if nome else ""
    nacionalidade = str(nacionalidade).strip() if nacionalidade else ""
    data_nascimento = str(data_nascimento).strip() if data_nascimento else ""

    if len(nome) < 2:
        return False, "O nome do diretor deve ter pelo menos 2 caracteres."

    if len(nacionalidade) < 2:
        return False, "A nacionalidade deve ter pelo menos 2 caracteres."

    if not data_nascimento:
        return False, "A data de nascimento é obrigatória."

    return True, ""

def validar_filme(titulo, ano, genero, diretor_id, nota, estudio):
    """Valida os dados de cadastro e edição do filme."""
    titulo = str(titulo).strip() if titulo else ""
    genero = str(genero).strip() if genero else ""
    estudio = str(estudio).strip() if estudio else ""
    ano_str = str(ano).strip() if ano else ""
    nota_str = str(nota).strip() if nota else ""
    diretor_str = str(diretor_id).strip() if diretor_id else ""

    if len(titulo) < 2:
        return False, "O título do filme deve ter pelo menos 2 caracteres."
    
    if len(genero) < 2:
        return False, "O gênero deve ter pelo menos 2 caracteres."
    
    if len(estudio) < 2:
        return False, "O nome do estúdio deve ter pelo menos 2 caracteres."

    if not diretor_str or not diretor_str.isdigit():
        return False, "Selecione um diretor válido na lista."

    try:
        ano_num = int(ano_str)
        if ano_num < 1888 or ano_num > 2026:
            return False, "O ano de lançamento deve estar entre 1888 e 2026."
    except ValueError:
        return False, "O ano deve conter apenas números inteiros."

    try:
        nota_num = float(nota_str)
        if nota_num < 0.0 or nota_num > 10.0:
            return False, "A nota deve ser um valor numérico entre 0.0 e 10.0."
    except ValueError:
        return False, "A nota deve ser um número válido (ex: 8.5)."

    return True, ""