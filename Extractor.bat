::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFDZdRwHVAES0A5EO4f7+08OKo0oYWvEDSJ3U3bWDIUPUSYbrSbAk2n9/gN8eDRhMcQCCbQA652dBuQQ=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFDZdRwHVAES0A5EO4f7+086IoVgQUewrd5zn6qaBJ+Ee6+Yj1lUi6l9CjNkNDw9XbFyudgpU
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
title Extrator de Arquivos
setlocal enabledelayedexpansion

:: Configuracoes
set "python_cmd=python"
set "python_script=extrator.py"

:: Verifica Python
where %python_cmd% >nul 2>&1 || (
    echo Python nao encontrado! Instale primeiro:
    echo https://www.python.org/downloads/
    timeout 10
    exit /b 1
)

:inicio
cls
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo  ARRASTE UMA PASTA PARA INICIAR A EXTRACAO
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo.

set "pasta="
set /p "pasta=Arraste a pasta para esta janela e pressione Enter: "

:: Remove aspas e valida
set "pasta=%pasta:"=%"
if "%pasta%"=="" (
    echo Nenhuma pasta selecionada!
    timeout 2
    goto inicio
)

if not exist "%pasta%" (
    echo Pasta invalida: "%pasta%"
    timeout 3
    goto inicio
)

echo Processando... Aguarde.
%python_cmd% "%python_script%" "%pasta%"

:: Mantem janela aberta mesmo apos erro
pause