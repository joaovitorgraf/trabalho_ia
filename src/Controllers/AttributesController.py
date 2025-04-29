from flask import request, jsonify

header = []
rgb = None
personagens = None


def Atributos():
    global header, rgb
    dados = request.get_json()

    if (
        not dados
        or "personagem" not in dados
        or "atributos" not in dados
        or "rgb" not in dados
        or "numero_atributos" not in dados
    ):
        return jsonify({"erro": "Dados inválidos"}), 400

    personagem = dados.get("personagem")
    atributos = dados.get("atributos")
    rgb = dados.get("rgb")
    numero_atributos = dados.get("numero_atributos")

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

    header.clear()
    for i, personagem_nome in enumerate(personagem):
        start_index = i * numero_atributos
        end_index = start_index + numero_atributos
        character_attributes = atributos[start_index:end_index]

        for attribute in character_attributes:
            name = f"{personagem_nome}_{attribute}"
            header.append(name)

    header.append("Classe")

    return jsonify({"sucesso": "Atributos definidos com sucesso."})


def get_header():
    return header


def get_rgb():
    return rgb


def get_personagens():
    return personagens
