@echo off
echo Verifying Application Status...

echo.
echo Checking if backend is running on http://localhost:8000...
curl -s -o nul -w "%%{http_code}" http://localhost:8000/health
echo.

echo.
echo You can also manually check:
echo - Backend API: http://localhost:8000/docs (Swagger UI)
echo - Backend Health: http://localhost:8000/health
echo - Frontend: http://localhost:3000 (usually)
echo.

echo If applications are not responding, please check:
echo 1. That the start-applications.bat script completed properly
echo 2. That no other processes are using ports 8000 or 3000
echo 3. That you have installed all dependencies for both backend and frontend
echo.

pause