from flask import request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import os
from PIL import Image


def Classificar_imagem_CNN():
    try:
        # Verifica se o modelo está salvo
        model_path = "modelos/cnn_model.keras"
        if not os.path.exists(model_path):
            return jsonify({"erro": "Rede ainda não foi treinada"}), 400

        # Verifica se o arquivo foi enviado
        if "imagem" not in request.files:
            return jsonify({"erro": "Nenhuma imagem foi enviada"}), 400

        arquivo = request.files["imagem"]
        if arquivo.filename == "":
            return jsonify({"erro": "Nome de arquivo inválido"}), 400

        # Salva temporariamente a imagem
        caminho_temporario = os.path.join("mediaCNN", "temp_classificacao.jpg")
        arquivo.save(caminho_temporario)

        # Carrega e pré-processa a imagem
        img = image.load_img(caminho_temporario, target_size=(64, 64))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normaliza como no treinamento

        # Carrega o modelo treinado
        modelo = load_model(model_path)

        # Previsão
        predicao = modelo.predict(img_array)
        indice_previsto = np.argmax(predicao)

        # Obtém os nomes das classes a partir da pasta de treino
        base_dir = "mediaCNN/base/training_set"
        classes = sorted(
            [
                nome
                for nome in os.listdir(base_dir)
                if os.path.isdir(os.path.join(base_dir, nome))
            ]
        )
        classe_prevista = (
            classes[indice_previsto]
            if indice_previsto < len(classes)
            else "Classe desconhecida"
        )

        # Remove a imagem temporária
        os.remove(caminho_temporario)

        return jsonify(
            {
                "classe_prevista": classe_prevista,
                "probabilidade": float(np.max(predicao)),
            }
        )

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
