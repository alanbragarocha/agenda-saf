@echo off
chcp 65001 >nul
echo ============================================
echo Criar Executável - Agenda Federação SAFs
echo ============================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo Por favor, instale Python 3.8 ou superior de https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado!
echo.

REM Instalar dependências
echo Instalando dependências...
pip install -r requirements.txt
pip install pyinstaller

if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependências!
    pause
    exit /b 1
)

echo.
echo [OK] Dependências instaladas!
echo.

REM Criar executável da GUI
echo Criando executável da Interface Gráfica...
pyinstaller --name="EditorAgendaSAF" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --add-data="agenda_data.json;." ^
    --add-data="gerar_agenda.py;." ^
    --add-data="gerar_com_fotos.py;." ^
    --add-data="extrair_fotos.py;." ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.scrolledtext ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=tkinter.simpledialog ^
    --hidden-import=docx ^
    --hidden-import=docx.shared ^
    --hidden-import=docx.enum.text ^
    --hidden-import=docx.oxml.ns ^
    --hidden-import=docx.oxml ^
    --hidden-import=docx.oxml.parser ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageTk ^
    --clean ^
    editar_agenda_gui.py

if errorlevel 1 (
    echo [ERRO] Falha ao criar executável!
    pause
    exit /b 1
)

echo.
echo ============================================
echo [SUCESSO] Executável criado!
echo ============================================
echo.
echo O arquivo executável está em: dist\EditorAgendaSAF.exe
echo.
echo IMPORTANTE: Copie o arquivo agenda_data.json para a mesma
echo pasta do executável para que o programa funcione corretamente.
echo.
pause
