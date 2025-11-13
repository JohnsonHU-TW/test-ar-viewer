@echo off
REM =================================================================
REM  Blender Conversion Batch File (V3 - "Factory Startup" Mode)
REM =================================================================
REM
REM This version adds the "--factory-startup" flag to force
REM Blender to ignore any corrupted user configuration files.
REM

setlocal
echo.

echo [1] Clearing all interfering environment variables...
set PYTHONPATH=
set PYTHONHOME=
echo     PYTHONPATH and PYTHONHOME have been cleared.
echo.

echo [2] Creating a minimal, clean PATH...
set BLENDER_DIR=C:\Program Files\Blender Foundation\Blender 4.5
set WIN_DIR=%SystemRoot%
set PATH=%WIN_DIR%\system32;%WIN_DIR%;%WIN_DIR%\System32\Wbem;%BLENDER_DIR%
echo     New temporary PATH is: %PATH%
echo.

echo [3] Defining file paths...
set BLENDER_EXE="%BLENDER_DIR%\blender.exe"
set SCRIPT_FILE="W:\vrview\blender_script.py"
set INPUT_FILE="W:\vrview\NCKU_Test_32.glb"
set OUTPUT_FILE="W:\vrview\NCKU_Test_32.usdz"
echo.

echo [4] Starting Blender background conversion...
echo     Adding "--factory-startup" to force a clean run.
echo.
echo     Executing: %BLENDER_EXE% --background --factory-startup --python %SCRIPT_FILE% -- %INPUT_FILE% %OUTPUT_FILE%
echo.
echo     --- Blender Output Starts ---

REM --- THIS IS THE KEY CHANGE ---
%BLENDER_EXE% --background --factory-startup --python %SCRIPT_FILE% -- %INPUT_FILE% %OUTPUT_FILE%

echo     --- Blender Output Ends ---
echo.

if %errorlevel% == 0 (
    echo [5] SUCCESS! (Exit Code 0)
    echo     File saved to: %OUTPUT_FILE%
) else (
    echo [5] ERROR: Conversion Failed! (Exit Code %errorlevel%)
    echo     Please review the Blender output above for details.
)

echo.
echo =================================================================
endlocal
pause