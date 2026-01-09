#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar a agenda com fotos de teste.
"""

import json
import os

# Carregar dados
with open('agenda_data.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Lista de fotos disponíveis
fotos_disponiveis = [
    'image1.jpeg', 'image2.jpeg', 'image3.jpeg', 'image4.png', 'image5.png',
    'image6.jpeg', 'image7.jpeg', 'image8.jpeg', 'image9.jpeg', 'image10.jpeg',
    'image11.jpeg', 'image12.png', 'image13.jpeg', 'image14.png', 'image15.jpeg',
    'image16.jpeg', 'image17.jpeg', 'image18.png', 'image19.jpeg', 'image20.jpeg',
    'image21.jpeg', 'image22.jpeg'
]

# Atribuir fotos aos membros da diretoria (primeiras 12 fotos)
for i, membro in enumerate(dados['diretoria']):
    if i < len(fotos_disponiveis):
        membro['foto'] = fotos_disponiveis[i]

# Atribuir fotos às SAFs (próximas fotos)
foto_idx = len(dados['diretoria'])
for saf in dados['safs']:
    if foto_idx < len(fotos_disponiveis):
        saf['foto'] = fotos_disponiveis[foto_idx]
        foto_idx += 1

# Atribuir foto ao missionário
if 'informacoes_gerais' in dados and 'missionario_oracao' in dados['informacoes_gerais']:
    if foto_idx < len(fotos_disponiveis):
        dados['informacoes_gerais']['missionario_oracao']['foto'] = fotos_disponiveis[foto_idx]

# Salvar JSON atualizado
with open('agenda_data_com_fotos.json', 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print("[OK] Dados atualizados com fotos salvos em: agenda_data_com_fotos.json")

# Gerar documento Word com as fotos
from gerar_agenda import gerar_agenda

gerar_agenda('agenda_data_com_fotos.json', 'Agenda 2024 - Com Fotos.docx')
