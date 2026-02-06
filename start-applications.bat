@echo off
echo Starting Full Stack Application...

REM Open a new command prompt for the backend
start "Backend Server" cmd /k "cd /d C:\Users\alish\Desktop\phase-03\backend && uvicorn main:app --reload --port 8000"

REM Wait a moment for the backend to start
timeout /t 5 /nobreak >nul

REM Open a new command prompt for the frontend
start "Frontend Server" cmd /k "cd /d C:\Users\alish\Desktop\phase-03\frontend && npm run dev"

echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000 (usually)
echo.
echo Press any key to exit...
pause >nul