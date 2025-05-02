import os
import csv
from PIL import Image
from ast import literal_eval
from flask import jsonify
from src.Controllers.AttributesController import get_header, get_rgb
from src.Controllers.MediaController import PASTA_MEDIA
from src.Controllers.ProgressoController import atualizar_progresso

TOLERANCIA = 15


def Gerar_csv():
    header = get_header()
    rgb = get_rgb()

    if not rgb or not header:
        return jsonify({"error": "Lista de RGBs ou Header não enviados!"}), 400

    mensagem = processar_imagens_e_gerar_csv(PASTA_MEDIA, rgb, header)
    atualizar_progresso(100)
    return jsonify({"mensagem": mensagem})


def cor_com_tolerancia(pixel, cor_referencia, tolerancia=TOLERANCIA):
    return all(abs(p - c) <= tolerancia for p, c in zip(pixel, cor_referencia))


def processar_imagens_e_gerar_csv(
    pasta_media, lista_rgb, header, nome_arquivo_saida="personagens.csv"
):
    lista_rgb = [literal_eval(rgb) for rgb in lista_rgb]
    dados_csv = []

    imagens = [
        os.path.join(d, f)
        for d, _, arquivos in os.walk(pasta_media)
        for f in arquivos
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp"))
    ]

    total = len(imagens)
    if total == 0:
        return "Nenhuma imagem encontrada!"

    for i, caminho_completo in enumerate(imagens):
        img = Image.open(caminho_completo).convert("RGB")
        largura, altura = img.size

        contador = {coluna: 0 for coluna in header if coluna != "Classe"}

        for x in range(largura):
            for y in range(altura):
                pixel = img.getpixel((x, y))
                for idx, cor_referencia in enumerate(lista_rgb):
                    if cor_com_tolerancia(pixel, cor_referencia):
                        coluna = header[idx]
                        contador[coluna] += 1

        pontuacao_por_personagem = {}
        for coluna in contador:
            if "_" in coluna:
                personagem, _ = coluna.split("_", 1)
                pontuacao_por_personagem[personagem] = (
                    pontuacao_por_personagem.get(personagem, 0) + contador[coluna]
                )

        classe_dominante = max(
            pontuacao_por_personagem, key=pontuacao_por_personagem.get
        )
        contador["Classe"] = classe_dominante
        dados_csv.append(contador)

        progresso = int(((i + 1) / total) * 100)
        atualizar_progresso(progresso)

    with open(nome_arquivo_saida, mode="w", newline="") as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=header)
        escritor.writeheader()
        for linha in dados_csv:
            escritor.writerow(linha)

    return f"Arquivo CSV '{nome_arquivo_saida}' criado com sucesso!"
