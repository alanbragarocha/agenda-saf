#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair fotos de um documento Word e salvá-las na pasta fotos.
"""

import os
import zipfile
import shutil
from docx import Document


def extrair_fotos_word(arquivo_word, pasta_destino='fotos'):
    """
    Extrai todas as imagens de um documento Word.

    Args:
        arquivo_word: Caminho do arquivo .docx
        pasta_destino: Pasta onde as imagens serão salvas
    """
    # Criar pasta de destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    # Documentos Word (.docx) são arquivos ZIP
    # As imagens ficam na pasta word/media/

    fotos_extraidas = []

    try:
        with zipfile.ZipFile(arquivo_word, 'r') as zip_ref:
            # Listar todos os arquivos no ZIP
            for nome_arquivo in zip_ref.namelist():
                # Verificar se é uma imagem na pasta media
                if nome_arquivo.startswith('word/media/'):
                    # Extrair nome do arquivo
                    nome_imagem = os.path.basename(nome_arquivo)

                    # Ler conteúdo da imagem
                    conteudo = zip_ref.read(nome_arquivo)

                    # Salvar na pasta de destino
                    caminho_destino = os.path.join(pasta_destino, nome_imagem)

                    with open(caminho_destino, 'wb') as f:
                        f.write(conteudo)

                    fotos_extraidas.append(nome_imagem)
                    print(f"  [OK] Extraída: {nome_imagem}")

        print(f"\n[OK] {len(fotos_extraidas)} foto(s) extraída(s) para a pasta '{pasta_destino}'")
        return fotos_extraidas

    except Exception as e:
        print(f"Erro ao extrair fotos: {e}")
        return []


def atualizar_json_com_fotos(fotos, arquivo_json='agenda_data.json'):
    """
    Atualiza o arquivo JSON com os caminhos das fotos extraídas.
    Tenta associar as fotos aos membros baseado na ordem.
    """
    import json

    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        print("\n[INFO] Fotos disponíveis para associação:")
        for i, foto in enumerate(fotos):
            print(f"  {i+1}. {foto}")

        # Não vamos atribuir automaticamente, apenas informar
        print("\n[INFO] Use a interface gráfica para associar as fotos aos membros.")
        print("       As fotos estão na pasta 'fotos/'")

        return True

    except Exception as e:
        print(f"Erro ao atualizar JSON: {e}")
        return False


if __name__ == "__main__":
    import sys

    # Arquivo Word padrão
    arquivo_word = "Agenda número 2023 (1).docx"

    # Verificar se foi passado um arquivo como argumento
    if len(sys.argv) > 1:
        arquivo_word = sys.argv[1]

    print(f"Extraindo fotos de: {arquivo_word}")
    print("-" * 50)

    if not os.path.exists(arquivo_word):
        print(f"Erro: Arquivo '{arquivo_word}' não encontrado!")
        sys.exit(1)

    # Extrair fotos
    fotos = extrair_fotos_word(arquivo_word)

    if fotos:
        # Informar sobre as fotos
        atualizar_json_com_fotos(fotos)
