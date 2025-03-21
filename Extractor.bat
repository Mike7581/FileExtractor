@echo off
chcp 65001
title Extrator de Arquivos
setlocal enabledelayedexpansion
color 0E

:: Verifica se o launcher "py" está instalado; caso não esteja, tenta o "python"
where py >nul 2>&1
if errorlevel 1 (
    where python >nul 2>&1
    if errorlevel 1 (
        echo Python não encontrado! Instale primeiro:
        echo https://www.python.org/downloads/
        timeout 10
        exit /b 1
    ) else (
        set "python_cmd=python"
    )
) else (
    set "python_cmd=py"
)

set "python_script=extrator.py"

:: Mensagens
set "msg_no_python=Python não encontrado! Instale primeiro:"
set "msg_invalid_folder=Pasta inválida: "
set "msg_no_folder=Nenhuma pasta selecionada!"
set "msg_decompile_prompt=Deseja decompilar arquivos .jar? (S/N): "
set "msg_processing=Processando... Aguarde."

:inicio
cls
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo  ARRASTE UMA PASTA PARA INICIAR A EXTRAÇÃO
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo.

:: Solicita a pasta ao usuário
set "pasta="
set /p "pasta=Arraste a pasta para esta janela e pressione Enter: "

:: Remove aspas e valida
set "pasta=%pasta:"=%"
if "%pasta%"=="" (
    echo %msg_no_folder%
    timeout 2
    goto inicio
)

if not exist "%pasta%" (
    echo %msg_invalid_folder% "%pasta%"
    timeout 3
    goto inicio
)

:: Verifica se há arquivos .jar na pasta
set "has_jar=0"
dir /s /b "%pasta%\*.jar" >nul 2>&1 && set "has_jar=1"

:: Pergunta sobre decompilação apenas se houver .jar
set "args="
if %has_jar% equ 1 (
    echo.
    :pergunta_decompile
    set "opcao="
    set /p "opcao=%msg_decompile_prompt%"
    if /i "%opcao%"=="S" (
        set "args=--decompile"
    ) else if /i "%opcao%"=="N" (
        set "args="
    ) else (
        echo Digite S ou N.
        goto pergunta_decompile
    )
)

:: Executa o script Python
echo %msg_processing%
%python_cmd% "%python_script%" "%pasta%" %args%

:: Mantém a janela aberta
pause
