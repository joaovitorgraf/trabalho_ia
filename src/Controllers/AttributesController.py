from flask import request, jsonify


def Atributos():
    dados = request.get_json()

    if (
        not dados
        or not "personagem" in dados
        or not "atributos" in dados
        or not "rgb" in dados
        or not "numero_atributos" in dados
    ):
        return jsonify({"erro": "Dados inválidos"}), 400

    personagem = dados.get("personagem")
    atributos = dados.get("atributos")
    rgb = dados.get("rgb")
    numero_atributos = dados.get("numero_atributos")

    if not personagem:
        return jsonify({"erro": "Personagem não pode estar vazio."}), 400

    tamanho_personagem = len(personagem)
    tamanho_atributos = len(atributos)
    rgb_size = len(rgb)

    if (tamanho_atributos / tamanho_personagem) != numero_atributos:
        return jsonify(
            {"erro": "O número de personagens não corresponde ao número de atributos."}
        )

    if tamanho_atributos < 3:
        return jsonify({"erro": "O número de atributos deve ser pelo menos três."})

    if tamanho_atributos < len(personagem) * numero_atributos:
        return jsonify(
            {"erro": "O número de atributos não corresponde ao tamanho do array."}
        )

    if tamanho_atributos != rgb_size:
        return (
            jsonify({"erro": "O número de atributos e cores não correspondem."}),
            400,
        )

    header = []

    for i, personagem in enumerate(personagem):
        start_index = i * numero_atributos
        end_index = start_index + numero_atributos
        character_attributes = atributos[start_index:end_index]

        for attribute in character_attributes:
            name = f"{personagem}_{attribute}"
            header.append(name)

    header.append("Classe")

    return jsonify({"sucesso": "Atributos definidos com sucesso."})
