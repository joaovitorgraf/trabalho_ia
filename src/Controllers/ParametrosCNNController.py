from flask import request, jsonify
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os


def Definir_parametros_e_treinar():
    try:
        dados = request.get_json()

        camadas = dados.get("camadas", 2)
        neuronios = dados.get("neuronios", 64)
        epocas = dados.get("epocas", 20)

        caminho_base = "mediaCNN"
        caminho_treino = os.path.join(caminho_base, "base/training_set")
        caminho_teste = os.path.join(caminho_base, "base/test_set")

        if not os.path.exists(caminho_treino) or not os.path.exists(caminho_teste):
            return jsonify({"erro": "Pastas de treino/teste não encontradas"}), 400

        gerador_treinamento = ImageDataGenerator(
            rescale=1.0 / 255, rotation_range=7, horizontal_flip=True, zoom_range=0.2
        )
        base_treinamento = gerador_treinamento.flow_from_directory(
            caminho_treino, target_size=(64, 64), batch_size=8, class_mode="categorical"
        )

        gerador_teste = ImageDataGenerator(rescale=1.0 / 255)
        base_teste = gerador_teste.flow_from_directory(
            caminho_teste,
            target_size=(64, 64),
            batch_size=8,
            class_mode="categorical",
            shuffle=False,
        )

        modelo = Sequential()

        for _ in range(camadas):
            modelo.add(Conv2D(32, (3, 3), activation="relu", input_shape=(64, 64, 3)))
            modelo.add(MaxPooling2D(pool_size=(2, 2)))

        modelo.add(Flatten())

        for _ in range(camadas):
            modelo.add(Dense(units=neuronios, activation="relu"))

        modelo.add(Dense(units=base_treinamento.num_classes, activation="softmax"))

        modelo.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )

        historico = modelo.fit(
            base_treinamento, epochs=epocas, validation_data=base_teste
        )

        os.makedirs("modelos", exist_ok=True)
        modelo.save("modelos/cnn_model.keras")

        acuracia = (
            historico.history.get("val_accuracy")[-1]
            if historico.history.get("val_accuracy")
            else None
        )

        return jsonify(
            {
                "mensagem": "Modelo treinado e salvo com sucesso",
                "epocas": epocas,
                "camadas": camadas,
                "neuronios": neuronios,
                "acuracia_validacao": round(acuracia * 100, 2) if acuracia else None,
            }
        )

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
