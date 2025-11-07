@echo off
REM HMH Content Management System - Start Backend Server
REM This script activates the virtual environment and starts the FastAPI backend

echo Starting HMH CMS Backend Server...
echo.

cd backend
call venv\Scripts\activate.bat
python main.py

pause
