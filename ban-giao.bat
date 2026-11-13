@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo === lam-net: chot phien M0 (kiem tra, commit, day len GitHub, tag m0) ===
set "GIT=git"
where git >nul 2>nul || set "GIT=C:\Program Files\Git\cmd\git.exe"
set "VPY=.venv312\Scripts\python.exe"
if not exist "outputs" mkdir outputs
set "LOG=outputs\ban-giao-log.txt"
set "MSG=%TEMP%\lam-net-commit-msg.txt"
set "TAG=m0"
echo ==== %DATE% %TIME% ==== > "%LOG%"

echo.
echo [1/4] Chay ca kiem chung...
if not exist "%VPY%" ( echo [LOI] Chua co .venv312 - chay chay-m0.bat truoc. & pause & exit /b 1 )
"%VPY%" validation\cases\test_duong_noi.py >> "%LOG%" 2>&1
findstr /C:"KET QUA: DAT" "%LOG%" >nul
if errorlevel 1 ( type "%LOG%" & echo [LOI] Ca kiem chung TRUOT - KHONG commit. Chup man hinh gui chi nhe. & pause & exit /b 1 )
echo    DAT

echo.
echo [2/4] Commit...
"%GIT%" add -- ".gitignore"
"%GIT%" add -- "README.md"
"%GIT%" add -- "RULES.md"
"%GIT%" add -- "CHANGELOG.md"
"%GIT%" add -- "HANDOVER.md"
"%GIT%" add -- "SOURCES.md"
"%GIT%" add -- "requirements.txt"
"%GIT%" add -- "chay-m0.bat"
"%GIT%" add -- "ban-giao.bat"
"%GIT%" add -- "docs/QA.md"
"%GIT%" add -- "engine/README.md"
"%GIT%" add -- "src/lam_net/engine.py"
"%GIT%" add -- "src/lam_net/tiling.py"
"%GIT%" add -- "src/lam_net/process.py"
"%GIT%" add -- "src/lam_net/cli.py"
"%GIT%" add -- "tools/pth_to_onnx.py"
"%GIT%" add -- "validation/cases/test_duong_noi.py"
type nul > "%MSG%"
>> "%MSG%" echo(M0: lõi làm nét chạy trên CPU, ghép ảnh dài không lộ đường nối
>> "%MSG%" echo(
>> "%MSG%" echo(- Mô hình Real-ESRGAN loại nhỏ (truyện / ảnh chụp) chuyển sang ONNX, chạy bằng ONNX Runtime CPU
>> "%MSG%" echo(- tools/pth_to_onnx.py: dựng ONNX từ .pth chính thức, không cần PyTorch
>> "%MSG%" echo(- tiling.py: cắt ô kèm đệm theo vùng ảnh hưởng, khớp tuyệt đối với chạy nguyên ảnh
>> "%MSG%" echo(- cli.py: dòng lệnh, mặc định 2×, đo thời gian/RAM, không ghi đè ảnh gốc
>> "%MSG%" echo(- Ca kiểm chứng đường nối; chay-m0.bat cài Python 3.12 64-bit + đo tốc độ; ban-giao.bat chốt phiên
>> "%MSG%" echo(- Ghi số đo trên máy em vào docs/QA.md; chốt mặc định 2× trong RULES.md
>> "%MSG%" echo(
>> "%MSG%" echo(Co-Authored-By: Claude Opus 5.5 ^<noreply@anthropic.com^>
>> "%MSG%" echo(Claude-Session: https://claude.ai/code/session_015Bc77m8Qtoj7MdvpGTFJ3u
"%GIT%" commit -F "%MSG%" >> "%LOG%" 2>&1
if errorlevel 1 ( type "%LOG%" & echo [LOI] Commit khong thanh cong. & pause & exit /b 1 )

echo.
echo [3/4] Dong bo va day len GitHub...
"%GIT%" pull --rebase origin main >> "%LOG%" 2>&1
if errorlevel 1 ( "%GIT%" rebase --abort >nul 2>nul & type "%LOG%" & echo [LOI] Xung dot khi dong bo - chua push. Chup man hinh gui chi nhe. & pause & exit /b 1 )
"%GIT%" push origin main >> "%LOG%" 2>&1
if errorlevel 1 ( type "%LOG%" & echo [LOI] Push khong thanh cong. & pause & exit /b 1 )

echo.
echo [4/4] Gan tag %TAG%...
"%GIT%" tag -a %TAG% -m "Moc %TAG%" >> "%LOG%" 2>&1
"%GIT%" push origin %TAG% >> "%LOG%" 2>&1
echo ---- trang thai ---- >> "%LOG%"
"%GIT%" status -sb >> "%LOG%" 2>&1
"%GIT%" log --oneline --decorate -3 >> "%LOG%" 2>&1
echo.
"%GIT%" status -sb
"%GIT%" log --oneline --decorate -3
echo.
echo [XONG] Da chot phien M0. Nhat ky: %LOG%
pause
