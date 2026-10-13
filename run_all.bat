@echo off
echo ===================================================
echo Scholarship Eligibility Assistant
echo ===================================================
echo Starting backend...
cd /d "%~dp0"
cd src\backend
pip install -q fastapi uvicorn --break-system-packages 2>nul
start "" python -m uvicorn src.app.main:app --host 0.0.0.0 --port 3000
timeout /t 3 /nobreak >nul
echo.
echo Backend running at http://localhost:3000
echo.
echo Starting frontend...
cd ../frontend
npm install vite --no-audit --no-fund 2>nul
npm run dev
pause
