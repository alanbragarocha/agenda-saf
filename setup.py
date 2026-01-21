#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script para instalação do Editor de Agenda - Federação de SAFs
"""

from setuptools import setup, find_packages
import os

# Ler o README para usar como descrição longa
long_description = """
Editor de Agenda para Federação de SAFs

Sistema completo para edição e geração de agendas em formato Word (.docx)
com suporte a fotos, formatação profissional e layout em duas colunas.

Recursos:
- Interface gráfica intuitiva (Tkinter)
- Edição completa de dados da agenda
- Geração automática de documentos Word
- Suporte a fotos e imagens
- Formatação profissional com layout em duas colunas
"""

setup(
    name="agenda-saf",
    version="1.0.0",
    description="Editor de Agenda para Federação de SAFs",
    long_description=long_description,
    author="Federação de SAFs",
    author_email="",
    url="",
    packages=find_packages(),
    py_modules=[
        "editar_agenda_gui",
        "gerar_agenda",
        "gerar_com_fotos",
        "extrair_fotos",
    ],
    install_requires=[
        "python-docx>=0.8.11",
        "Pillow>=10.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "agenda-editor=editar_agenda_gui:main",
            "agenda-gerar=gerar_agenda:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "agenda_data.json",
            "requirements.txt",
            "README.md",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
    ],
)
