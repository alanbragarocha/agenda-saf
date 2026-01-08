#!/bin/bash
# Script de instalação das dependências

echo "Instalando dependências do sistema de automação da agenda..."
pip3 install -r requirements.txt
echo "✓ Instalação concluída!"
echo ""
echo "Para gerar a agenda, execute:"
echo "  python3 gerar_agenda.py"
echo ""
echo "Para editar os dados, execute:"
echo "  python3 editar_agenda.py"
