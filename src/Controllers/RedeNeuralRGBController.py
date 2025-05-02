import os
import tensorflow as tf
import pandas as pd
import numpy as np
from flask import request, jsonify, Blueprint
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from werkzeug.utils import secure_filename
from PIL import Image

rede_neural_bp = Blueprint("rede_neural", __name__)
modelo = None
nomes_classes = []


def Treinar_modelo():
    global modelo, nomes_classes

    dados = request.json
    camadas = int(dados.get("camadas"))
    neuronios = int(dados.get("neuronios"))
    epocas = int(dados.get("epocas"))

    df = pd.read_csv("personagens.csv")

    X = df.iloc[:, 0:6].values
    y_raw = df.iloc[:, 6].values
    nomes_classes = sorted(np.unique(y_raw))
    y_map = {nome: idx for idx, nome in enumerate(nomes_classes)}
    y = np.array([y_map[nome] for nome in y_raw])
    y = to_categorical(y)

    X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(
        X, y, test_size=0.2
    )

    modelo = tf.keras.models.Sequential()
    modelo.add(
        tf.keras.layers.Dense(units=neuronios, activation="relu", input_shape=(6,))
    )

    for _ in range(camadas - 1):
        modelo.add(tf.keras.layers.Dense(units=neuronios, activation="relu"))

    modelo.add(tf.keras.layers.Dense(units=len(nomes_classes), activation="softmax"))

    modelo.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    modelo.fit(
        X_treinamento, y_treinamento, epochs=epocas, validation_split=0.1, verbose=0
    )

    _, acuracia = modelo.evaluate(X_teste, y_teste, verbose=0)

    modelo.save("modelos/rgb_model.keras")

    return jsonify(
        {
            "mensagem": "Modelo treinado com sucesso!",
            "classes": nomes_classes,
            "acuracia": round(float(acuracia), 4),
        }
    )


def Classificar_imagem():
    global modelo, nomes_classes

    if modelo is None:
        if not os.path.exists("modelos/rgb_model.keras"):
            return (
                jsonify(
                    {"erro": "Modelo não treinado. Use a rota /parametros primeiro."}
                ),
                400,
            )

        modelo = tf.keras.models.load_model("modelos/rgb_model.keras")
        df = pd.read_csv("personagens.csv")
        nome_coluna_classe = df.columns[-1]
        nomes_classes = sorted(df[nome_coluna_classe].unique())

    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhuma imagem foi enviada."}), 400

    imagem = request.files["imagem"]
    caminho = os.path.join("uploads", secure_filename(imagem.filename))
    os.makedirs("uploads", exist_ok=True)
    imagem.save(caminho)

    atributos = extrair_atributos(caminho)
    entrada = np.array([atributos])

    predicao = modelo.predict(entrada)
    indice_previsto = np.argmax(predicao)
    nome_previsto = nomes_classes[indice_previsto]
    probabilidade = float(np.max(predicao))

    return jsonify(
        {"classe_prevista": nome_previsto, "probabilidade": round(probabilidade, 4)}
    )


def extrair_atributos(caminho_imagem):
    imagem = Image.open(caminho_imagem).resize((64, 64)).convert("RGB")
    np_img = np.array(imagem).reshape(-1, 3)
    r_mean = np.mean(np_img[:, 0])
    g_mean = np.mean(np_img[:, 1])
    b_mean = np.mean(np_img[:, 2])
    r_std = np.std(np_img[:, 0])
    g_std = np.std(np_img[:, 1])
    b_std = np.std(np_img[:, 2])
    return [r_mean, g_mean, b_mean, r_std, g_std, b_std]
