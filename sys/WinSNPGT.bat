@echo off

"%~dp0"\URL.lnk

setlocal enableextensions
set TERM=

del "%~dp0\home\%USERNAME%\.bashrc"
copy "%~dp0\bashrc.SNPGT" "%~dp0\home\%USERNAME%\.bashrc" > nul
cd /d "%~dp0\bin" && .\bash --login -i