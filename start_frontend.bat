@echo off
title EVOLUTION TRACKER 2.0 - Frontend Client
echo ===================================================
echo   EVOLUTION TRACKER 2.0 - VISION X FRONTEND
echo   VERIFY BEFORE YOU SHARE
echo ===================================================
cd /d "%~dp0"
set PATH=%~dp0.tools\node;%PATH%
cd frontend
call npm run dev -- --host
pause
