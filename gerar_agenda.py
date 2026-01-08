#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar automaticamente a Agenda da Federação de SAFs
a partir de um arquivo JSON estruturado.
"""

import json
from datetime import datetime
try:
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
except ImportError:
    print("Instalando python-docx...")
    import subprocess
    subprocess.check_call(["pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn


def configurar_estilo_paragrafo(paragrafo, tamanho=11, negrito=False, italico=False,
                                alinhamento=WD_ALIGN_PARAGRAPH.LEFT, espacamento_antes=0,
                                espacamento_depois=0):
    """Configura o estilo de um parágrafo"""
    paragrafo.alignment = alinhamento
    paragrafo.paragraph_format.space_before = Pt(espacamento_antes)
    paragrafo.paragraph_format.space_after = Pt(espacamento_depois)

    for run in paragrafo.runs:
        run.font.size = Pt(tamanho)
        run.font.bold = negrito
        run.font.italic = italico
        run.font.name = 'Calibri'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')


def adicionar_titulo(doc, texto, nivel=1):
    """Adiciona um título ao documento"""
    p = doc.add_paragraph()
    p.add_run(texto).bold = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    configurar_estilo_paragrafo(p, tamanho=14 if nivel == 1 else 12, negrito=True,
                                espacamento_antes=12, espacamento_depois=6)


def adicionar_texto_formatado(doc, texto, tamanho=11, negrito=False, italico=False,
                               alinhamento=WD_ALIGN_PARAGRAPH.LEFT):
    """Adiciona texto formatado ao documento"""
    p = doc.add_paragraph()
    run = p.add_run(texto)
    run.bold = negrito
    run.italic = italico
    run.font.size = Pt(tamanho)
    p.alignment = alinhamento
    configurar_estilo_paragrafo(p, tamanho=tamanho, negrito=negrito, italico=italico,
                                alinhamento=alinhamento)


def gerar_agenda(data_file='agenda_data.json', output_file=None):
    """Gera o documento Word da agenda a partir do JSON"""

    # Carregar dados
    with open(data_file, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    # Criar documento
    doc = Document()

    # Configurar seções
    section = doc.sections[0]
    section.page_height = Inches(11.69)  # A4
    section.page_width = Inches(8.27)
    section.left_margin = Inches(0.98)
    section.right_margin = Inches(0.98)
    section.top_margin = Inches(0.98)
    section.bottom_margin = Inches(0.98)

    # Título principal
    adicionar_titulo(doc, f"Agenda {dados['ano']}", nivel=1)
    doc.add_paragraph()  # Espaço

    # Palavra da Presidente
    adicionar_titulo(doc, "Palavra da Presidente", nivel=2)
    adicionar_texto_formatado(doc, dados['presidente']['mensagem'], tamanho=11)
    doc.add_paragraph()
    adicionar_texto_formatado(doc, dados['presidente']['nome'], tamanho=11, negrito=True,
                             alinhamento=WD_ALIGN_PARAGRAPH.RIGHT)
    doc.add_paragraph()  # Espaço

    # Diretoria
    adicionar_titulo(doc, "I – Diretoria", nivel=2)

    for membro in dados['diretoria']:
        linha = f"{membro['cargo']}: {membro['nome']}"
        if membro.get('data_nascimento'):
            linha += f"\nDN - {membro['data_nascimento']}"
        if membro.get('email'):
            linha += f"\nE-mail: {membro['email']}"
        if membro.get('endereco'):
            linha += f"\nEnd: {membro['endereco']}"
        adicionar_texto_formatado(doc, linha, tamanho=11)
        doc.add_paragraph()  # Espaço

    # SAFs
    adicionar_titulo(doc, "III – Safs", nivel=2)

    for saf in dados['safs']:
        # Número e nome da SAF
        adicionar_texto_formatado(doc, f"{saf['numero']}- {saf['nome']}",
                                 tamanho=11, negrito=True)
        adicionar_texto_formatado(doc, f"End: {saf['endereco']}", tamanho=11)

        # Pastor
        if saf.get('pastor'):
            pastor = saf['pastor']
            linha_pastor = f"Pastor da Igreja: {pastor['nome']}"
            if pastor.get('data_nascimento'):
                linha_pastor += f" ({pastor['data_nascimento']})"
            adicionar_texto_formatado(doc, linha_pastor, tamanho=11)

        # Presidente
        if saf.get('presidente'):
            pres = saf['presidente']
            adicionar_texto_formatado(doc, f"Presidente: {pres['nome']}", tamanho=11)
            if pres.get('data_nascimento'):
                adicionar_texto_formatado(doc, f"({pres['data_nascimento']})", tamanho=11)
            if pres.get('endereco'):
                adicionar_texto_formatado(doc, f"End: {pres['endereco']}", tamanho=11)
            if pres.get('cep'):
                adicionar_texto_formatado(doc, f"Cep: {pres['cep']}", tamanho=11)
            if pres.get('telefone'):
                adicionar_texto_formatado(doc, pres['telefone'], tamanho=11)
            if pres.get('email'):
                adicionar_texto_formatado(doc, f"@{pres['email']}", tamanho=11)

        # Conselheiro
        if saf.get('conselheiro') and saf['conselheiro'].get('nome'):
            cons = saf['conselheiro']
            linha_cons = f"Conselheiro(a): {cons['nome']}"
            if cons.get('data_nascimento'):
                linha_cons += f" ({cons['data_nascimento']})"
            adicionar_texto_formatado(doc, linha_cons, tamanho=11)

        # Aniversário
        if saf.get('aniversario'):
            aniv = saf['aniversario']
            adicionar_texto_formatado(doc,
                f"Aniversário da Saf – {aniv['data']} - {aniv['anos']} Anos",
                tamanho=11)

        doc.add_paragraph()  # Espaço entre SAFs

    # Atividades Realizadas
    adicionar_titulo(doc, "IV – Atividades Realizadas em 2023", nivel=2)
    for atividade in dados['atividades_realizadas_2023']:
        linha = atividade['descricao']
        if atividade.get('data'):
            linha = f"{atividade['data']} – {linha}"
        adicionar_texto_formatado(doc, linha, tamanho=11)

    doc.add_paragraph()  # Espaço

    # Atividades Planejadas
    adicionar_titulo(doc, "V- ATIVIDADES A SEREM REALIZADAS EM 2024", nivel=2)

    meses_pt = {
        'janeiro': 'Janeiro', 'fevereiro': 'Fevereiro', 'marco': 'Março',
        'abril': 'Abril', 'maio': 'Maio', 'junho': 'Junho',
        'julho': 'Julho', 'agosto': 'Agosto', 'setembro': 'Setembro',
        'outubro': 'Outubro', 'novembro': 'Novembro', 'dezembro': 'Dezembro'
    }

    for mes_key, mes_nome in meses_pt.items():
        if mes_key in dados['atividades_planejadas_2024']:
            adicionar_texto_formatado(doc, mes_nome, tamanho=11, negrito=True)
            for atividade in dados['atividades_planejadas_2024'][mes_key]:
                linha = atividade['descricao']
                if atividade.get('data'):
                    linha = f"{atividade['data']} – {linha}"
                adicionar_texto_formatado(doc, linha, tamanho=11)
            doc.add_paragraph()  # Espaço

    # Informações Gerais
    adicionar_titulo(doc, "Informações Gerais", nivel=2)

    if dados.get('informacoes_gerais'):
        info = dados['informacoes_gerais']

        if info.get('missionario_oracao'):
            miss = info['missionario_oracao']
            adicionar_texto_formatado(doc, "Nome do Missionário de Oração:", tamanho=11, negrito=True)
            adicionar_texto_formatado(doc, f"- Rev. {miss['nome']} ({miss['data_nascimento']})", tamanho=11)
            adicionar_texto_formatado(doc, f"Campo: {miss['campo']}", tamanho=11)
            adicionar_texto_formatado(doc, f"WhatsApp: {miss['whatsapp']}", tamanho=11)
            doc.add_paragraph()

        if info.get('observacoes'):
            adicionar_texto_formatado(doc, "Obs:", tamanho=11, negrito=True)
            for obs in info['observacoes']:
                adicionar_texto_formatado(doc, f"  - {obs}", tamanho=11)
            doc.add_paragraph()

        if info.get('lema'):
            for linha in info['lema']:
                adicionar_texto_formatado(doc, linha, tamanho=11,
                                         alinhamento=WD_ALIGN_PARAGRAPH.CENTER)

    # Anotações Gerais
    doc.add_page_break()
    adicionar_titulo(doc, "Anotações Gerais", nivel=2)
    for _ in range(20):  # Linhas para anotações
        p = doc.add_paragraph("_" * 100)
        configurar_estilo_paragrafo(p, tamanho=11)

    # Salvar documento
    if output_file is None:
        output_file = f"Agenda {dados['ano']}.docx"

    doc.save(output_file)
    print(f"✓ Documento gerado com sucesso: {output_file}")


if __name__ == "__main__":
    import sys

    data_file = sys.argv[1] if len(sys.argv) > 1 else 'agenda_data.json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        gerar_agenda(data_file, output_file)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{data_file}' não encontrado!")
        print("Certifique-se de que o arquivo JSON existe no diretório atual.")
    except Exception as e:
        print(f"Erro ao gerar agenda: {e}")
        import traceback
        traceback.print_exc()
