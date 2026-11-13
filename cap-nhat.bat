@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "GIT=git"
where git >nul 2>nul || set "GIT=C:\Program Files\Git\cmd\git.exe"
echo === Cap nhat lam-net tu GitHub ===
"%GIT%" pull --ff-only origin main
if errorlevel 1 (
  echo.
  echo [LOI] Chua keo ve duoc. Chup man hinh gui chi nhe.
) else (
  echo.
  echo [XONG] Da cap nhat ban moi nhat.
)
"%GIT%" log --oneline --decorate -3
pause
