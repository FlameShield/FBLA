@echo off
setlocal

set "python=python3.10"
for /f "tokens=*" %%i in ('where %python%') do set "python=%%i"

set "file=%~dp0Script+data\FBLA_PROJECTs.py"
call "%python%" "%file%"

pause

