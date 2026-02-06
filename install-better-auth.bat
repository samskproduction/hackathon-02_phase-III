@echo off
echo Installing Better Auth dependencies...

cd frontend

REM Install Better Auth packages
npm install better-auth better-auth/react

REM Install development dependencies if needed
npm install -D @types/better-auth

echo Better Auth dependencies installed successfully!
echo.
echo Next steps:
echo 1. Update your backend to work with Better Auth (if needed)
echo 2. Configure Better Auth in your backend
echo 3. Run 'npm run dev' to start the frontend
pause