@echo off
chcp 65001 >nul
title Instalador - Editor de Agenda SAFs
color 0A

echo.
echo ================================================================
echo     INSTALADOR - EDITOR DE AGENDA FEDERAÇÃO DE SAFs
echo ================================================================
echo.
echo Este instalador vai:
echo   1. Verificar se o Python está instalado
echo   2. Instalar todas as dependências necessárias
echo   3. Criar atalhos no menu Iniciar
echo   4. Configurar o programa para uso
echo.
echo ================================================================
echo.

REM Verificar se Python está instalado
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python não encontrado!
    echo.
    echo Por favor, instale Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante a instalação, marque a opção
    echo "Add Python to PATH" para que o Python seja encontrado.
    echo.
    echo Pressione qualquer tecla para abrir o site de download...
    pause >nul
    start https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% encontrado!
echo.

REM Atualizar pip
echo [2/4] Atualizando pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [AVISO] Não foi possível atualizar o pip, continuando...
)
echo [OK] Pip atualizado!
echo.

REM Instalar dependências
echo [3/4] Instalando dependências...
echo    - python-docx (manipulação de documentos Word)
echo    - Pillow (processamento de imagens)
echo.
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar dependências!
    echo Tente executar manualmente: pip install -r requirements.txt
    pause
    exit /b 1
)
echo [OK] Dependências instaladas!
echo.

REM Criar diretório de instalação
set INSTALL_DIR=%LOCALAPPDATA%\AgendaSAFs
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copiar arquivos necessários
echo [4/4] Copiando arquivos...
copy /Y "editar_agenda_gui.py" "%INSTALL_DIR%\" >nul
copy /Y "gerar_agenda.py" "%INSTALL_DIR%\" >nul
copy /Y "gerar_com_fotos.py" "%INSTALL_DIR%\" >nul
copy /Y "extrair_fotos.py" "%INSTALL_DIR%\" >nul
if exist "agenda_data.json" copy /Y "agenda_data.json" "%INSTALL_DIR%\" >nul
if exist "fotos" xcopy /E /I /Y "fotos" "%INSTALL_DIR%\fotos" >nul

REM Criar scripts de inicialização
echo @echo off > "%INSTALL_DIR%\EditorAgenda.bat"
echo cd /d "%%~dp0" >> "%INSTALL_DIR%\EditorAgenda.bat"
echo python editar_agenda_gui.py >> "%INSTALL_DIR%\EditorAgenda.bat"
echo pause >> "%INSTALL_DIR%\EditorAgenda.bat"

REM Criar atalho no menu Iniciar (se possível)
set START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs
if exist "%START_MENU%" (
    echo @echo off > "%START_MENU%\Editor Agenda SAFs.bat"
    echo cd /d "%INSTALL_DIR%" >> "%START_MENU%\Editor Agenda SAFs.bat"
    echo python editar_agenda_gui.py >> "%START_MENU%\Editor Agenda SAFs.bat"
    echo pause >> "%START_MENU%\Editor Agenda SAFs.bat"
)

echo [OK] Arquivos copiados!
echo.

REM Criar arquivo de configuração
echo {"instalado": true, "versao": "1.0.0", "data_instalacao": "%DATE%"} > "%INSTALL_DIR%\instalacao.json"

echo ================================================================
echo     INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo ================================================================
echo.
echo O programa foi instalado em:
echo %INSTALL_DIR%
echo.
echo Para executar o programa:
echo   1. Menu Iniciar ^> Editor Agenda SAFs
echo   2. Ou execute: python editar_agenda_gui.py
echo.
echo Arquivos de dados serão salvos em:
echo %INSTALL_DIR%
echo.
echo ================================================================
echo.
pause
