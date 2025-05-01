import os
import shutil
import zipfile
import rarfile
import random
import stat
from flask import request, jsonify

MEDIA_PATH = "mediaCNN"
TEMP_PATH = os.path.join(MEDIA_PATH, "temp_upload")
TRAIN_DIR = os.path.join(MEDIA_PATH, "base/training_set")
TEST_DIR = os.path.join(MEDIA_PATH, "base/test_set")


def remover_com_permissao(pasta):
    def onerror(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(pasta, onerror=onerror)


def Upload_e_separar():
    if "arquivo" not in request.files:
        return jsonify({"erro": "Arquivo não enviado"}), 400

    arquivo = request.files["arquivo"]
    if arquivo.filename == "":
        return jsonify({"erro": "Nome de arquivo inválido"}), 400

    extensao = arquivo.filename.rsplit(".", 1)[1].lower()
    if extensao not in ["zip", "rar"]:
        return (
            jsonify({"erro": "Formato não suportado. Envie um arquivo .zip ou .rar"}),
            400,
        )

    # Limpar diretórios anteriores
    for pasta in [TEMP_PATH, TRAIN_DIR, TEST_DIR]:
        if os.path.exists(pasta):
            remover_com_permissao(pasta)
        os.makedirs(pasta)

    # Salvar temporariamente
    caminho_arquivo = os.path.join(TEMP_PATH, arquivo.filename)
    arquivo.save(caminho_arquivo)

    # Extrair
    if extensao == "zip":
        with zipfile.ZipFile(caminho_arquivo, "r") as zip_ref:
            zip_ref.extractall(TEMP_PATH)
    elif extensao == "rar":
        with rarfile.RarFile(caminho_arquivo, "r") as rar_ref:
            rar_ref.extractall(TEMP_PATH)

    # Separar em treino e teste
    PORCENTAGEM_TESTE = 0.2  # 20% para teste
    classes = os.listdir(TEMP_PATH)
    for classe in classes:
        caminho_classe = os.path.join(TEMP_PATH, classe)
        if not os.path.isdir(caminho_classe):
            continue

        imagens = os.listdir(caminho_classe)
        random.shuffle(imagens)

        qtd_teste = int(len(imagens) * PORCENTAGEM_TESTE)
        imagens_teste = imagens[:qtd_teste]
        imagens_treino = imagens[qtd_teste:]

        for img in imagens_treino:
            origem = os.path.join(caminho_classe, img)
            destino = os.path.join(TRAIN_DIR, classe)
            os.makedirs(destino, exist_ok=True)
            shutil.copy(origem, os.path.join(destino, img))

        for img in imagens_teste:
            origem = os.path.join(caminho_classe, img)
            destino = os.path.join(TEST_DIR, classe)
            os.makedirs(destino, exist_ok=True)
            shutil.copy(origem, os.path.join(destino, img))

    return (
        jsonify({"mensagem": "Imagens carregadas, extraídas e separadas com sucesso."}),
        200,
    )
