@echo off
echo ============================================
echo   CALENDARIO YPF - Iniciando Servidores
echo ============================================
echo.

echo [0/3] Cerrando servidores anteriores...
taskkill /F /FI "WINDOWTITLE eq Backend YPF*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Frontend YPF*" >nul 2>&1
echo Servidores anteriores cerrados.
timeout /t 2 /nobreak >nul

echo.
echo [1/3] Iniciando Backend (Puerto 8000)...
start "Backend YPF" cmd /k "cd backend && python app_flask.py"
timeout /t 3 /nobreak >nul

echo [2/3] Iniciando Frontend (Puerto 5173)...
start "Frontend YPF" cmd /k "cd frontend && python server.py"
timeout /t 3 /nobreak >nul

echo [3/3] Abriendo navegador...
start http://localhost:5173

echo.
echo ============================================
echo   APLICACION INICIADA!
echo ============================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo IMPORTANTE:
echo - Se abrieron 2 ventanas (Backend y Frontend)
echo - NO cierres esas ventanas mientras uses la app
echo - Para detener, cierra las ventanas o presiona Ctrl+C
echo.
pause
