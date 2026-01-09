#!/bin/bash

echo "============================================"
echo "Criar Executável - Agenda Federação SAFs"
echo "============================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 não encontrado!"
    echo "Por favor, instale Python 3.8 ou superior"
    exit 1
fi

echo "[OK] Python encontrado!"
echo ""

# Instalar dependências
echo "Instalando dependências..."
pip3 install -r requirements.txt
pip3 install pyinstaller

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao instalar dependências!"
    exit 1
fi

echo ""
echo "[OK] Dependências instaladas!"
echo ""

# Criar executável da GUI
echo "Criando executável da Interface Gráfica..."
pyinstaller --name="EditorAgendaSAF" \
    --onefile \
    --windowed \
    --add-data="agenda_data.json:." \
    --hidden-import=tkinter \
    --hidden-import=tkinter.ttk \
    --hidden-import=tkinter.scrolledtext \
    --hidden-import=tkinter.filedialog \
    --hidden-import=tkinter.messagebox \
    --hidden-import=tkinter.simpledialog \
    --hidden-import=docx \
    --hidden-import=docx.shared \
    --hidden-import=docx.enum.text \
    --hidden-import=docx.oxml.ns \
    --clean \
    editar_agenda_gui.py

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao criar executável!"
    exit 1
fi

echo ""
echo "============================================"
echo "[SUCESSO] Executável criado!"
echo "============================================"
echo ""
echo "O arquivo executável está em: dist/EditorAgendaSAF"
echo ""
echo "IMPORTANTE: Copie o arquivo agenda_data.json para a mesma"
echo "pasta do executável para que o programa funcione corretamente."
echo ""
