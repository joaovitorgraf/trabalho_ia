import os
import zipfile
import rarfile
from flask import request, jsonify

rarfile.UNRAR_TOOL = r"C:\Program Files\UnRAR\UnRAR.exe"

PASTA_MEDIA = "media"
if not os.path.exists(PASTA_MEDIA):
    os.makedirs(PASTA_MEDIA)


def Upload():
    if "arquivo" not in request.files:
        return jsonify({"erro": "Nenhum arquivo foi enviado."}), 400

    arquivo = request.files["arquivo"]

    if arquivo.filename == "":
        return jsonify({"erro": "Nenhum arquivo selecionado."}), 400

    if not (arquivo.filename.endswith(".zip") or arquivo.filename.endswith(".rar")):
        return jsonify({"erro": "O arquivo precisa ser um ZIP ou RAR."}), 400

    try:
        caminho_arquivo = os.path.join(PASTA_MEDIA, arquivo.filename)
        arquivo.save(caminho_arquivo)

        if arquivo.filename.endswith(".zip"):
            with zipfile.ZipFile(caminho_arquivo, "r") as zip_ref:
                zip_ref.extractall(PASTA_MEDIA)

        elif arquivo.filename.endswith(".rar"):
            with rarfile.RarFile(caminho_arquivo, "r") as rar_ref:
                rar_ref.extractall(PASTA_MEDIA)

        os.remove(caminho_arquivo)

        return jsonify({"sucesso": "Arquivo descompactado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def get_urlImage(pasta_base=PASTA_MEDIA):
    caminhos_imagens = {}

    for root, _, arquivos in os.walk(pasta_base):
        imagens = [
            os.path.abspath(os.path.join(root, nome_arquivo)).replace("\\", "/")
            for nome_arquivo in arquivos
            if nome_arquivo.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        ]

        if imagens:
            # nome da pasta que contém as imagens
            nome_pasta = os.path.basename(root)
            if nome_pasta not in caminhos_imagens:
                caminhos_imagens[nome_pasta] = []

            caminhos_imagens[nome_pasta].extend(imagens)

    return jsonify({"sucesso": caminhos_imagens}), 200
