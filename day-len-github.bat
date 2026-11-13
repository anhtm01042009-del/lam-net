@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Day du an lam-net len GitHub ===

set "GIT=git"
where git >nul 2>nul
if not errorlevel 1 goto CO_GIT

if exist "C:\Program Files\Git\cmd\git.exe" (
  set "GIT=C:\Program Files\Git\cmd\git.exe"
  goto CO_GIT
)

echo May chua co Git. Dang cai Git chinh thuc bang winget...
echo (Neu Windows hoi quyen quan tri, em bam Yes.)
where winget >nul 2>nul
if errorlevel 1 (
  echo [LOI] May khong co winget. Em tai Git tai https://git-scm.com/download/win , cai xong chay lai file nay.
  pause
  exit /b 1
)
winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
if not exist "C:\Program Files\Git\cmd\git.exe" (
  echo [LOI] Cai Git chua thanh cong. Chup man hinh gui chi nhe.
  pause
  exit /b 1
)
set "GIT=C:\Program Files\Git\cmd\git.exe"

:CO_GIT
if not exist ".git" "%GIT%" init -b main

set "GUN="
for /f "delims=" %%a in ('"%GIT%" config user.name') do set "GUN=%%a"
if not defined GUN "%GIT%" config user.name "anhtm01042009-del"
set "GUE="
for /f "delims=" %%a in ('"%GIT%" config user.email') do set "GUE=%%a"
if not defined GUE "%GIT%" config user.email "anhtm01042009-del@users.noreply.github.com"

"%GIT%" add .
"%GIT%" commit -m "Khoi dong du an lam-net: khung thu muc, quy tac, ghi chep"

"%GIT%" remote remove origin >nul 2>nul
"%GIT%" remote add origin https://github.com/anhtm01042009-del/lam-net.git
"%GIT%" branch -M main
"%GIT%" push -u origin main

if errorlevel 1 (
  echo.
  echo [LOI] Push khong thanh cong. Chup man hinh cua so nay gui chi nhe.
) else (
  echo.
  echo [XONG] Da day len https://github.com/anhtm01042009-del/lam-net
)
pause
