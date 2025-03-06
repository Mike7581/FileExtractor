@echo off
title Extrator de Arquivos
:inicio
cls
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo  ARRASTE AQUI UMA PASTA PARA EXTRAIR
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo.
set "pasta="
set /p "pasta=Arraste a pasta para esta janela e pressione Enter: "

REM Verifica se o usuário digitou algo
if "%pasta%"=="" (
    echo Nenhuma pasta foi selecionada. Reiniciando...
    timeout 3 /nobreak >nul
    goto inicio
    exit
)

REM Remove aspas extras (caso o usuário arraste a pasta)
set "pasta=%pasta:"=%"

REM Verifica se a pasta existe
if not exist "%pasta%" (
    echo A pasta "%pasta%" não foi encontrada. Saindo...
    timeout 3 /nobreak >nul
    exit
)

REM Cria pasta de destino
set "nome_pasta=Arquivos da pasta %~nxpasta%"
set "pasta_destino=%cd%\%nome_pasta%"
mkdir "%pasta_destino%" 2>nul

REM Inicia a extração
echo Extraindo arquivos...
setlocal enabledelayedexpansion
set "contador=0"
for /r "%pasta%" %%f in (*) do (
    set /a contador+=1
    copy "%%f" "%pasta_destino%\" >nul
    echo %%f >> "%pasta_destino%\lista_arquivos.txt"
)

REM Exibe resultado
echo.
echo Pronto! ^>
echo - %contador% arquivos extraídos para a pasta "%nome_pasta%".
echo - Lista de nomes salva em "%nome_pasta%\lista_arquivos.txt".
echo.

REM Pergunta se quer continuar
:pergunta
echo Deseja processar outra pasta? (S/N)
set /p "resposta="
if /i "%resposta%"=="s" (
    goto inicio
) else if /i "%resposta%"=="n" (
    exit
) else (
    echo Digite S ou N.
    goto pergunta
)