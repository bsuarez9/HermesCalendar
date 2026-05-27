@echo off
echo ============================================
echo   CALENDARIO YPF - Deteniendo Servidores
echo ============================================
echo.

echo Cerrando Backend...
taskkill /F /FI "WINDOWTITLE eq Backend YPF*" >nul 2>&1

echo Cerrando Frontend...
taskkill /F /FI "WINDOWTITLE eq Frontend YPF*" >nul 2>&1

echo.
echo ============================================
echo   Servidores detenidos correctamente!
echo ============================================
echo.
pause
