@echo off

REM Check if Python 3.10 is installed
python --version | findstr /C:"Python 3.10" >nul

if %errorlevel% == 0 (
    echo Python 3.10 is already installed.
) else (
    echo Installing Python 3.10...
    REM Download Python 3.10 installer
    curl -o python-3.10.0-amd64.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    
    REM Install Python 3.10
    python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
    
    echo Python 3.10 has been installed.
)