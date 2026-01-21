@echo off
chcp 65001 >nul
title Criar Instalador - Editor de Agenda SAFs
color 0B

echo.
echo ================================================================
echo     CRIAR INSTALADOR - EDITOR DE AGENDA SAFs
echo ================================================================
echo.
echo Este script vai criar um instalador profissional para Windows.
echo.
echo Opções disponíveis:
echo   1. Criar executável .exe (PyInstaller)
echo   2. Criar instalador Inno Setup (requer Inno Setup instalado)
echo   3. Criar ambos
echo.
echo ================================================================
echo.

set /p opcao="Escolha uma opção (1, 2 ou 3): "

if "%opcao%"=="1" goto criar_exe
if "%opcao%"=="2" goto criar_innosetup
if "%opcao%"=="3" goto criar_ambos
goto fim

:criar_exe
echo.
echo [1/2] Criando executável .exe...
call criar_executavel.bat
goto fim

:criar_innosetup
echo.
echo [1/2] Verificando Inno Setup...
where iscc >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Inno Setup não encontrado!
    echo.
    echo Por favor, instale Inno Setup de:
    echo https://jrsoftware.org/isinfo.php
    echo.
    pause
    exit /b 1
)

echo [OK] Inno Setup encontrado!
echo.
echo [2/2] Compilando instalador...
iscc instalador.iss
if errorlevel 1 (
    echo [ERRO] Falha ao compilar instalador!
    pause
    exit /b 1
)

echo.
echo [SUCESSO] Instalador criado em: dist\InstaladorAgendaSAFs.exe
goto fim

:criar_ambos
echo.
echo Criando executável e instalador...
call criar_executavel.bat
echo.
echo Aguarde...
timeout /t 2 >nul
call :criar_innosetup
goto fim

:fim
echo.
echo ================================================================
echo     PROCESSO CONCLUÍDO!
echo ================================================================
echo.
pause
