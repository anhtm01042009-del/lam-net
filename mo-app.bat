@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set "VPY=.venv312\Scripts\python.exe"
echo === Mo app Lam Net ===
if not exist "%VPY%" (
  echo Chua co moi truong .venv312 - dang chay chay-m0.bat de cai lan dau...
  call chay-m0.bat
)
if not exist "%VPY%" ( echo [LOI] Chua cai duoc moi truong. & pause & exit /b 1 )

"%VPY%" -c "import PySide6" >nul 2>nul
if errorlevel 1 (
  echo Lan dau mo app: dang cai thu vien giao dien PySide6 - vai phut, khong hien chu...
  "%VPY%" -m pip install -r requirements.txt
  if errorlevel 1 ( echo [LOI] Cai PySide6 that bai. Chup man hinh gui chi nhe. & pause & exit /b 1 )
)
if not exist "engine\realesr-animevideov3.onnx" ( echo [LOI] Thieu file mo hinh trong engine\ - xem engine\README.md & pause & exit /b 1 )

echo Dang mo app... (dong cua so app thi cua so nay cung tu dong)
"%VPY%" src\lam_net\gui.py
if errorlevel 1 (
  echo.
  echo [LOI] App bi loi khi chay - chup man hinh cua so nay gui chi nhe.
  pause
)
