@echo off
chcp 65001 >nul
cd /d "%~dp0"

py -3 --version >nul 2>nul
if %errorlevel%==0 (
  py -3 pro_trial.py --ask-lang
) else (
  python --version >nul 2>nul
  if %errorlevel%==0 (
    python pro_trial.py --ask-lang
  ) else (
    echo [ERR] Python 3.10+ not found in PATH.
    echo Download: https://www.python.org/downloads/ (check Add python.exe to PATH)
  )
)

echo.
pause
