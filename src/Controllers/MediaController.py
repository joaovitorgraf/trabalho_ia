import os
import zipfile
from flask import request, jsonify

PASTA_MEDIA = "media"
if not os.path.exists(PASTA_MEDIA):
    os.makedirs(PASTA_MEDIA)


def Upload():
    if "arquivo" not in request.files:
        return jsonify({"erro": "Nenhum arquivo foi enviado."}), 400

    arquivo = request.files["arquivo"]

    if arquivo.filename == "":
        return jsonify({"erro": "Nenhum arquivo selecionado."})

    if not arquivo.filename.endswith(".zip"):
        return jsonify({"erro": "O arquivo precisa ser um ZIP."}), 400

    try:
        zip_path = os.path.join(PASTA_MEDIA, arquivo.filename)

        arquivo.save(zip_path)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(PASTA_MEDIA)

        os.remove(zip_path)

        return jsonify({"sucesso": "Arquivo descompactado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
