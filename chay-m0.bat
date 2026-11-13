@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo === lam-net M0: cai moi truong, kiem tra, do toc do ===

rem Python dang co trong may (chi de ghi nhan)
echo Python mac dinh trong may:
py -3 -c "import sys,struct;print('  ',sys.version.split()[0], struct.calcsize('P')*8,'bit')" 2>nul || echo    (khong co py launcher)

rem ---- 1. Tim Python 3.12 ban 64-bit (onnxruntime can ban nay) ----
set "PY312=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
set "PY="
py -3.12-64 -c "import sys" >nul 2>nul && set "PY=py -3.12-64"
if not defined PY if exist "%PY312%" set "PY="%PY312%""
if defined PY goto CO_PY

echo Chua co Python 3.12 64-bit. Dang cai ban chinh thuc bang winget...
winget install -e --id Python.Python.3.12 --scope user --architecture x64 --source winget --accept-package-agreements --accept-source-agreements
if exist "%PY312%" (
  set "PY="%PY312%""
) else (
  echo [LOI] Cai Python 3.12 chua thanh cong. Chup man hinh gui chi nhe.
  pause & exit /b 1
)

:CO_PY
echo Dung Python:
%PY% -c "import sys,struct;print('  ',sys.version.split()[0], struct.calcsize('P')*8,'bit')"

rem ---- 2. Moi truong rieng .venv312 + thu vien ----
set "VPY=.venv312\Scripts\python.exe"
if not exist "%VPY%" (
  echo Tao moi truong .venv312 ...
  %PY% -m venv .venv312
)
if not exist "%VPY%" ( echo [LOI] Khong tao duoc .venv312 & pause & exit /b 1 )
echo Cai thu vien (lan dau mat vai phut, khong hien chu trong luc cai)...
"%VPY%" -m pip install -q --upgrade pip
"%VPY%" -m pip install -q -r requirements.txt
if errorlevel 1 ( echo [LOI] Cai thu vien that bai. Chup man hinh gui chi nhe. & pause & exit /b 1 )

if not exist "outputs" mkdir outputs
set "LOG=outputs\ket-qua-m0.txt"
echo ==== %DATE% %TIME% ==== > "%LOG%"
"%VPY%" -c "import sys,platform;print('Python',sys.version.split()[0],platform.machine())" >> "%LOG%"
"%VPY%" -m pip freeze >> "%LOG%"

rem ---- 3. Ca kiem chung duong noi ----
echo.
echo [1/2] Kiem tra duong noi...
"%VPY%" validation\cases\test_duong_noi.py >> "%LOG%" 2>&1
type "%LOG%" | findstr /C:"DAT" /C:"TRUOT" /C:"Error" /C:"LOI"

rem ---- 4. Do toc do tren anh that ----
echo.
echo [2/2] Do toc do (anh dai co the mat vai phut, em cu de may chay)...
set "DAI=samples\tay_20261113_194221_phan1_20261113_194221.png"
"%VPY%" src\lam_net\cli.py "%DAI%" --scale 2 --do --log "%LOG%"
"%VPY%" src\lam_net\cli.py "%DAI%" --scale 4 --do --log "%LOG%"
"%VPY%" src\lam_net\cli.py samples\vung_20261113_194045.png --kieu anh --scale 4 --do --log "%LOG%"
"%VPY%" src\lam_net\cli.py "%DAI%" --scale 4 --nhanh --do --log "%LOG%"

echo.
echo [XONG] Ket qua da luu vao %LOG%. Anh lam net nam trong thu muc outputs.
echo Em nhan voi chi la "xong" de chi doc ket qua nhe.
pause
