@echo off
chcp 65001 >nul
echo ========================================
echo   Subiendo cambios a RAMA-3...
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Agregando archivos...
git add -A
echo.

echo [2/3] Haciendo commit...
git commit -m "feat: Rediseno del perfil cliente, eliminacion de foto_banner y logica de roles"
echo.

echo [3/3] Subiendo a GitHub (RAMA-3)...
git push origin RAMA-3
echo.

echo ========================================
echo   LISTO! Cambios subidos a RAMA-3
echo ========================================
echo.
pause
