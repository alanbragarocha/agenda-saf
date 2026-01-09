@echo off
chcp 65001 >nul
echo ============================================
echo Instalação - Agenda Federação SAFs
echo ============================================
echo.
echo Este script vai instalar o Python e as dependências necessárias.
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Python não encontrado!
    echo.
    echo Por favor, instale Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante a instalação, marque a opção
    echo "Add Python to PATH" para que o Python seja encontrado.
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado!
python --version
echo.

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Instalar dependências
echo Instalando dependências do projeto...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependências!
    pause
    exit /b 1
)

echo.
echo ============================================
echo [SUCESSO] Instalação concluída!
echo ============================================
echo.
echo Agora você pode executar o programa:
echo   - Interface Gráfica: python editar_agenda_gui.py
echo   - Interface Web: python editar_agenda_web.py
echo   - Gerar Word: python gerar_agenda.py
echo.
echo Para criar um executável .exe, execute: criar_executavel.bat
echo.
pause
