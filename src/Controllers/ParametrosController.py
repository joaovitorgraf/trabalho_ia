from flask import request, jsonify
from src.tasks.ActionRedeNeuralRGB import treinar_rede

camadas = None
neuronios = None
epocas = None


def Parametros():
    global camadas, neuronios, epocas
    dados = request.get_json()

    if (
        not dados
        or not "camadas" in dados
        or not "neuronios" in dados
        or not "epocas" in dados
    ):
        return jsonify({"erro": "Dados inválidos"}), 400

    camadas = int(dados.get("camadas"))
    neuronios = int(dados.get("neuronios"))
    epocas = int(dados.get("epocas"))

    if camadas <= 0:
        return jsonify({"erro": "Camadas não pode ser 0 ou menor."}), 400

    if neuronios <= 0:
        return jsonify({"erro": "Neuronios não ser 0 ou menor."}), 400

    if epocas <= 0:
        return jsonify({"erro": "Epocas não ser 0 ou menor."}), 400

    resultado = treinar_rede(camadas, neuronios, epocas)
    return jsonify(resultado), 200
