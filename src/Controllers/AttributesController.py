from flask import request, jsonify


def attributes():
    dados = request.get_json()

    if not dados or not "attributes" in dados or not "rgb" in dados:
        return jsonify({"error": "Invalid data"}), 400

    character = dados.get("character")
    attributes = dados.get("attributes")
    rgb = dados.get("rgb")
    number_attributes = dados.get("number_attributes")

    if not character:
        return jsonify({"error": "Character cannot be empty."}), 400

    attributes_size = len(attributes)
    rgb_size = len(rgb)

    if attributes_size < 3:
        return jsonify({"error": "The number of attributes must be at least three."})

    if attributes_size < len(character) * number_attributes:
        return jsonify(
            {"error": "The number of attributes does not match the size of the array."}
        )

    if attributes_size != rgb_size:
        return (
            jsonify({"error": "The number of attributes and colors do not match."}),
            400,
        )

    header = []

    for i, character in enumerate(character):
        start_index = i * number_attributes
        end_index = start_index + number_attributes
        character_attributes = attributes[start_index:end_index]

        for attribute in character_attributes:
            name = f"{character}_{attribute}"
            header.append(name)

    header.append("Classe")
    print(header)

    return jsonify({"success": "Attributes set successfully."})
