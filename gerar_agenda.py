#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar automaticamente a Agenda da Federação de SAFs
a partir de um arquivo JSON estruturado.
Formato: Folder vertical com 2 colunas e linha divisória no centro.
"""

import json
import os
from datetime import datetime

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor, Twips
except ImportError:
    print("Instalando python-docx...")
    import subprocess

    subprocess.check_call(["pip", "install", "python-docx"])
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor, Twips


def configurar_colunas_secao(
    section, num_colunas=2, espacamento=0.3, linha_divisoria=True
):
    """
    Configura a seção para ter múltiplas colunas com linha divisória.
    """
    sectPr = section._sectPr

    # Remover configuração de colunas existente
    cols_existente = sectPr.find(qn('w:cols'))
    if cols_existente is not None:
        sectPr.remove(cols_existente)

    # Criar novo elemento de colunas
    cols = OxmlElement('w:cols')
    cols.set(qn('w:num'), str(num_colunas))
    cols.set(qn('w:space'), str(int(espacamento * 1440)))

    if linha_divisoria:
        cols.set(qn('w:sep'), '1')

    sectPr.append(cols)


def adicionar_titulo_secao(doc, texto):
    """Adiciona um título de seção principal (centralizado, negrito, Arial 14)"""
    p = doc.add_paragraph()
    run = p.add_run(texto)
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Arial'
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    return p


def adicionar_subtitulo(doc, texto):
    """Adiciona um subtítulo (negrito, alinhado à esquerda, Arial 12)"""
    p = doc.add_paragraph()
    run = p.add_run(texto)
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Arial'
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    return p


def adicionar_texto(doc, texto, tamanho=12, negrito=False, italico=False):
    """Adiciona texto compacto (Arial 12)"""
    p = doc.add_paragraph()
    run = p.add_run(texto)
    run.font.size = Pt(tamanho)
    run.font.name = 'Arial'
    run.bold = negrito
    run.italic = italico
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    return p


def adicionar_linha(doc, texto, tamanho=12):
    """Adiciona uma linha de texto (Arial 12)"""
    p = doc.add_paragraph()
    run = p.add_run(texto)
    run.font.size = Pt(tamanho)
    run.font.name = 'Arial'
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    return p


def adicionar_espaco(doc, pts=6):
    """Adiciona um espaço vertical controlado"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(pts)
    return p


def adicionar_imagem(doc, caminho_imagem, largura_base=None):
    """
    Adiciona uma imagem ao documento Word no formato 3x4.
    """
    if not caminho_imagem:
        return False

    try:
        caminho_final = None

        if os.path.isabs(caminho_imagem):
            caminho_final = caminho_imagem
        else:
            try:
                pasta_atual = os.path.dirname(os.path.abspath(data_file_path))
            except:
                pasta_atual = os.path.dirname(os.path.abspath('agenda_data.json'))

            pasta_fotos = os.path.join(pasta_atual, 'fotos')

            caminhos_tentar = [
                os.path.join(pasta_fotos, caminho_imagem),
                os.path.join(pasta_atual, caminho_imagem),
                caminho_imagem,
            ]

            for caminho in caminhos_tentar:
                if os.path.exists(caminho):
                    caminho_final = caminho
                    break

        if not caminho_final or not os.path.exists(caminho_final):
            return False

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)

        if largura_base is None:
            largura_base = Inches(0.7)

        # Proporção 3x4 (largura:altura = 3:4)
        largura = largura_base
        altura = Inches(largura_base.inches * (4 / 3))

        run = p.add_run()
        run.add_picture(caminho_final, width=largura, height=altura)
        return True
    except Exception as e:
        return False


# Variável global para armazenar o caminho do arquivo de dados
data_file_path = 'agenda_data.json'


def gerar_agenda(data_file='agenda_data.json', output_file=None):
    """Gera o documento Word da agenda a partir do JSON"""

    global data_file_path
    data_file_path = os.path.abspath(data_file)

    # Carregar dados
    with open(data_file, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    doc = Document()

    # Configurar página - A4 paisagem
    section = doc.sections[0]
    section.page_height = Inches(8.27)
    section.page_width = Inches(11.69)
    section.left_margin = Inches(0.4)
    section.right_margin = Inches(0.4)
    section.top_margin = Inches(0.4)
    section.bottom_margin = Inches(0.4)

    # CONFIGURAR 2 COLUNAS COM LINHA DIVISÓRIA NO CENTRO
    configurar_colunas_secao(
        section, num_colunas=2, espacamento=0.25, linha_divisoria=True
    )

    # ==================== CONTEÚDO ====================

    # === PALAVRA DA PRESIDENTE ===
    adicionar_titulo_secao(doc, "PALAVRA DA PRESIDENTE")

    mensagem = dados['presidente']['mensagem'].replace('\n\n', '\n').strip()
    adicionar_texto(doc, mensagem, tamanho=10)
    adicionar_texto(doc, dados['presidente']['nome'], tamanho=10, negrito=True)
    adicionar_espaco(doc, 8)

    # === DIRETORIA ===
    adicionar_titulo_secao(doc, "I - DIRETORIA")

    for membro in dados['diretoria']:
        if membro.get('nome'):
            # Foto pequena
            if membro.get('foto'):
                adicionar_imagem(doc, membro['foto'], largura_base=Inches(0.5))

            # Cargo e Nome
            cargo_nome = f"{membro['cargo']}: {membro['nome']}"
            if membro.get('data_nascimento'):
                cargo_nome += f" (DN: {membro['data_nascimento']})"
            adicionar_linha(doc, cargo_nome)

            # Email e endereço em uma linha (se houver)
            detalhes = []
            if membro.get('email'):
                detalhes.append(membro['email'])
            if membro.get('endereco'):
                detalhes.append(membro['endereco'])
            if detalhes:
                adicionar_linha(doc, " | ".join(detalhes), tamanho=10)

    adicionar_espaco(doc, 8)

    # === SAFs ===
    adicionar_titulo_secao(doc, "II - SAFs FILIADAS")

    for saf in dados['safs']:
        # Título da SAF
        adicionar_subtitulo(doc, f"{saf['numero']}. {saf['nome']}")

        # Foto da SAF (menor)
        if saf.get('foto'):
            adicionar_imagem(doc, saf['foto'], largura_base=Inches(0.6))

        # Endereço
        adicionar_linha(doc, f"End: {saf['endereco']}")

        # Pastor
        if saf.get('pastor') and saf['pastor'].get('nome'):
            pastor = saf['pastor']
            linha = f"Pastor: {pastor['nome']}"
            if pastor.get('data_nascimento'):
                linha += f" ({pastor['data_nascimento']})"
            adicionar_linha(doc, linha)

        # Presidente
        if saf.get('presidente') and saf['presidente'].get('nome'):
            pres = saf['presidente']
            linha_pres = f"Presidente: {pres['nome']}"
            if pres.get('data_nascimento'):
                linha_pres += f" ({pres['data_nascimento']})"
            adicionar_linha(doc, linha_pres)

            # Contato
            contato = []
            if pres.get('telefone'):
                contato.append(pres['telefone'])
            if pres.get('email'):
                contato.append(pres['email'])
            if contato:
                adicionar_linha(doc, "Contato: " + " | ".join(contato), tamanho=10)

        # Conselheiro
        if saf.get('conselheiro') and saf['conselheiro'].get('nome'):
            cons = saf['conselheiro']
            linha_cons = f"Conselheiro: {cons['nome']}"
            if cons.get('data_nascimento'):
                linha_cons += f" ({cons['data_nascimento']})"
            adicionar_linha(doc, linha_cons)

        # Aniversário
        if saf.get('aniversario'):
            aniv = saf['aniversario']
            adicionar_linha(doc, f"Aniversário: {aniv['data']} - {aniv['anos']} anos")

        adicionar_espaco(doc, 4)

    # === ATIVIDADES REALIZADAS ===
    adicionar_titulo_secao(doc, "III - ATIVIDADES REALIZADAS EM 2023")

    for atividade in dados.get('atividades_realizadas_2023', []):
        linha = atividade['descricao']
        if atividade.get('data'):
            linha = f"{atividade['data']} - {linha}"
        adicionar_linha(doc, f"• {linha}")

    adicionar_espaco(doc, 8)

    # === ATIVIDADES PLANEJADAS ===
    ano_atual = dados.get('ano', 2024)
    adicionar_titulo_secao(doc, f"IV - ATIVIDADES PLANEJADAS PARA {ano_atual}")

    meses_pt = {
        'janeiro': 'JANEIRO',
        'fevereiro': 'FEVEREIRO',
        'marco': 'MARÇO',
        'abril': 'ABRIL',
        'maio': 'MAIO',
        'junho': 'JUNHO',
        'julho': 'JULHO',
        'agosto': 'AGOSTO',
        'setembro': 'SETEMBRO',
        'outubro': 'OUTUBRO',
        'novembro': 'NOVEMBRO',
        'dezembro': 'DEZEMBRO',
    }

    chave_atividades = f'atividades_planejadas_{ano_atual}'
    atividades_planejadas = dados.get(chave_atividades, {})

    for mes_key, mes_nome in meses_pt.items():
        if mes_key in atividades_planejadas and atividades_planejadas[mes_key]:
            adicionar_subtitulo(doc, mes_nome)

            for atividade in atividades_planejadas[mes_key]:
                linha = atividade['descricao']
                if atividade.get('data'):
                    linha = f"{atividade['data']} - {linha}"
                adicionar_linha(doc, f"• {linha}")

    adicionar_espaco(doc, 8)

    # === INFORMAÇÕES GERAIS ===
    adicionar_titulo_secao(doc, "V - INFORMAÇÕES GERAIS")

    if dados.get('informacoes_gerais'):
        info = dados['informacoes_gerais']

        # Missionário de Oração
        if info.get('missionario_oracao'):
            miss = info['missionario_oracao']
            adicionar_subtitulo(doc, "Missionário de Oração:")

            if miss.get('foto'):
                adicionar_imagem(doc, miss['foto'], largura_base=Inches(0.6))

            adicionar_linha(
                doc,
                f"Rev. {miss.get('nome', '')} (DN: {miss.get('data_nascimento', '')})",
            )
            adicionar_linha(
                doc,
                f"Campo: {miss.get('campo', '')} | WhatsApp: {miss.get('whatsapp', '')}",
            )
            adicionar_espaco(doc, 4)

        # Observações
        if info.get('observacoes'):
            adicionar_subtitulo(doc, "Observações:")
            for obs in info['observacoes']:
                adicionar_linha(doc, f"• {obs}")
            adicionar_espaco(doc, 4)

        # Lema
        if info.get('lema'):
            adicionar_subtitulo(doc, "Lema:")
            for linha in info['lema']:
                p = adicionar_linha(doc, linha)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Salvar documento
    if output_file is None:
        output_file = f"Agenda {dados['ano']}.docx"

    doc.save(output_file)
    print(f"[OK] Documento gerado com sucesso: {output_file}")


if __name__ == "__main__":
    import sys

    data_file = sys.argv[1] if len(sys.argv) > 1 else 'agenda_data.json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        gerar_agenda(data_file, output_file)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{data_file}' não encontrado!")
    except Exception as e:
        print(f"Erro ao gerar agenda: {e}")
        import traceback

        traceback.print_exc()
