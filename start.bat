@echo off
title Community Hero Launcher

echo.
echo  ==========================================
echo   Community Hero - Starting Services...
echo  ==========================================
echo.

echo  [1/2] Starting Flask Backend on port 5000...
start "Community Hero - Backend" cmd /k "cd /d c:\Community Hero\backend && py app.py"

timeout /t 2 /nobreak >nul

echo  [2/2] Starting Frontend Server on port 8080...
start "Community Hero - Frontend" cmd /k "py -m http.server 8080 --directory c:\Community Hero\frontend"

timeout /t 2 /nobreak >nul

echo  [3/3] Opening Dashboard in browser...
start "" "http://localhost:8080/dashboard.html"

echo.
echo  ==========================================
echo   Done! Community Hero is running.
echo   Backend:  http://localhost:5000
echo   Frontend: http://localhost:8080/dashboard.html
echo  ==========================================
echo.
echo  Close the two terminal windows to stop.
pause
