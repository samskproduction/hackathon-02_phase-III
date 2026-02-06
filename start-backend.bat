@echo off
echo Starting Backend Server...

REM Navigate to backend directory
cd backend

REM Start the backend server
uvicorn main:app --reload --port 8000