@echo off
setlocal
cd /d "%~dp0"
title KILLER
color 0C

where python >nul 2>nul
if %errorlevel% equ 0 (
    python killer.py
    goto end
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    py killer.py
    goto end
)

echo [!] Python is not installed or not added to PATH.
echo [!] Please install Python from https://www.python.org and check "Add Python to PATH".

:end
echo.
pause
