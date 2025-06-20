@echo off
title Limpeza de Arquivos Temporarios do Usuario
color 0A
echo ===============================================
echo    Limpeza de Arquivos Temporarios do Usuario
echo ===============================================
echo.

echo Iniciando limpeza dos arquivos temporarios...
echo.

:: Limpa a pasta Temp do usuario atual
echo Limpando pasta Temp do usuario...
del /f /s /q "%TEMP%\*.*" 2>nul
for /d %%i in ("%TEMP%\*") do rd /s /q "%%i" 2>nul

:: Limpa a pasta Recent (documentos recentes)
echo Limpando pasta de documentos recentes...
del /f /s /q "%APPDATA%\Microsoft\Windows\Recent\*.*" 2>nul
for /d %%i in ("%APPDATA%\Microsoft\Windows\Recent\*") do rd /s /q "%%i" 2>nul

:: Limpa arquivos temporarios do Internet Explorer/Edge
echo Limpando arquivos temporarios do navegador...
del /f /s /q "%LOCALAPPDATA%\Microsoft\Windows\INetCache\*.*" 2>nul
for /d %%i in ("%LOCALAPPDATA%\Microsoft\Windows\INetCache\*") do rd /s /q "%%i" 2>nul

:: Limpa pasta de downloads do Windows Update
echo Limpando arquivos temporarios do usuario...
del /f /s /q "%LOCALAPPDATA%\Temp\*.*" 2>nul
for /d %%i in ("%LOCALAPPDATA%\Temp\*") do rd /s /q "%%i" 2>nul

echo.
echo Limpeza concluida com sucesso!
echo.
echo Pressione qualquer tecla para sair...
pause >nul 