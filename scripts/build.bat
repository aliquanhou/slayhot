@echo off
REM scripts\build.bat 鈥?SlayHot 鏋勫缓鑴氭湰锛圵indows锛?
REM 鐢ㄦ硶: scripts\build.bat [harness|py|all]

echo === SlayHot Build Script ===
echo.

if "%1"=="py" goto build_py
if "%1"=="harness" goto build_harness
if "%1"=="all" goto build_all

:build_all
call :build_py
call :build_harness
goto end

:build_harness
echo [Build] Go Harness...
cd /d "%~dp0..\harness"
echo   -> Windows x64
set GOOS=windows
set GOARCH=amd64
go build -ldflags="-s -w" -o "..\@SlayHot\harness-win32-x64\bin\SlayHot.exe" .
cd /d "%~dp0.."
echo   [OK] Harness build complete
goto :EOF

:build_py
echo [Build] Python Core...
cd /d "%~dp0.."
python -c "import sys; sys.path.insert(0,'.'); from agent.core import Agent; from agent.tools import get_all_tools; print(f'  [OK] Python core imports OK, tools: {len(get_all_tools())}')" || echo [FAIL]
goto :EOF

:end
echo.
echo === Build Complete ===
