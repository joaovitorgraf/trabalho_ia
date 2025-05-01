import os
import numpy as np
import tensorflow as tf
from flask import request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image

# Variáveis globais para cache
modelo = None
personagens = None


def carregar_recursos():
    global modelo, personagens
    if modelo is None and os.path.exists("modelo_rede_neural.keras"):
        modelo = tf.keras.models.load_model("modelo_rede_neural.keras")
    if personagens is None and os.path.exists("personagens.npy"):
        personagens = np.load("personagens.npy", allow_pickle=True).tolist()


def extrair_atributos_imagem(caminho_imagem):
    try:
        img = Image.open(caminho_imagem).convert("RGB")
        img = img.resize((64, 64))  # Redimensionar para tamanho consistente

        # Converter para array e normalizar
        pixels = np.array(img) / 255.0

        # Extrair características (simplificado - deve ser igual ao usado no treino)
        # Aqui você deve implementar a mesma lógica usada para gerar o CSV
        atributos = [
            np.mean(pixels[:, :, 0]),  # R
            np.mean(pixels[:, :, 1]),  # G
            np.mean(pixels[:, :, 2]),  # B
            0.5,  # Mock - substituir por atributos reais
            0.5,  # Mock - substituir por atributos reais
            0.5,  # Mock - substituir por atributos reais
        ]

        return np.array([atributos])
    except Exception as e:
        raise Exception(f"Erro ao processar imagem: {str(e)}")


def classificar_imagem():
    carregar_recursos()

    if modelo is None or personagens is None:
        return jsonify({"erro": "Modelo não treinado ou não encontrado"}), 400

    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    imagem = request.files["imagem"]
    if imagem.filename == "":
        return jsonify({"erro": "Nome de arquivo inválido"}), 400

    # Criar diretório temporário se não existir
    os.makedirs("media/temp", exist_ok=True)
    caminho = os.path.join("media/temp", secure_filename(imagem.filename))
    imagem.save(caminho)

    try:
        # Extrair atributos da imagem
        X_imagem = extrair_atributos_imagem(caminho)

        # Fazer previsão
        probabilidade = float(modelo.predict(X_imagem)[0][0])
        classe = personagens[0] if probabilidade > 0.5 else personagens[1]

        return jsonify(
            {
                "classe": classe,
                "probabilidade": (
                    probabilidade if classe == personagens[0] else 1 - probabilidade
                ),
                "personagens": personagens,
            }
        )
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if os.path.exists(caminho):
            os.remove(caminho)
