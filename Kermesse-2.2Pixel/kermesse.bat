@echo off
rem Lanzador para Windows: doble clic, o en la terminal:  kermesse.bat --lento
cd /d "%~dp0src"
python chat.py %*
if errorlevel 1 pause
