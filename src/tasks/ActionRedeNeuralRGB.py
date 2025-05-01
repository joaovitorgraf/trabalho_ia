import os
import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix


def treinar_rede(camadas: int, neuronios: int, epocas: int):
    try:
        # Carregar dataset
        caminho_csv = os.path.join(os.getcwd(), "personagens.csv")
        dataset = pd.read_csv(caminho_csv)

        # Verificar estrutura do dataset
        if dataset.shape[1] < 7:  # 6 atributos + 1 classe
            return {"erro": "Estrutura do CSV inválida"}, 400

        # Preparar dados
        X = dataset.iloc[:, 0:6].values
        y = dataset.iloc[:, 6].values

        # Converter classes para binário (assume que a classe é o primeiro personagem)
        personagens = sorted(list(set(y)))
        y = y == personagens[0]  # Primeiro personagem como classe positiva

        # Dividir dados
        X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Construir modelo
        rede_neural = tf.keras.models.Sequential()

        # Camada de entrada
        rede_neural.add(
            tf.keras.layers.Dense(units=neuronios, activation="relu", input_shape=(6,))
        )

        # Camadas ocultas
        for _ in range(camadas - 1):
            rede_neural.add(tf.keras.layers.Dense(units=neuronios, activation="relu"))

        # Camada de saída
        rede_neural.add(tf.keras.layers.Dense(units=1, activation="sigmoid"))

        # Compilar e treinar
        rede_neural.compile(
            optimizer="Adam", loss="binary_crossentropy", metrics=["accuracy"]
        )

        historico = rede_neural.fit(
            X_treinamento, y_treinamento, epochs=epocas, validation_split=0.1, verbose=0
        )

        # Avaliar
        previsoes = rede_neural.predict(X_teste) > 0.5
        acuracia = accuracy_score(y_teste, previsoes)
        matriz_confusao = confusion_matrix(y_teste, previsoes).tolist()

        # Salvar modelo
        rede_neural.save("modelo_rede_neural.keras")

        # Salvar informações dos personagens
        np.save("personagens.npy", np.array(personagens))

        return {
            "acuracia": float(acuracia),
            "matriz_confusao": matriz_confusao,
            "personagens": personagens,
            "personagem_alvo": personagens[0],
            "historico": {
                "loss": historico.history["loss"],
                "accuracy": historico.history["accuracy"],
                "val_loss": historico.history.get("val_loss", []),
                "val_accuracy": historico.history.get("val_accuracy", []),
            },
        }

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
