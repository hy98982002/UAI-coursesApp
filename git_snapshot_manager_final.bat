@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo       Git Snapshot Manager (Final)
echo ==========================================
echo.
echo Choose an option:
echo   1. Save current snapshot
echo   2. Restore latest snapshot
echo   3. Select and restore from history
echo.

set /p choice=Enter your choice (1 / 2 / 3): 

IF "%choice%"=="1" GOTO SAVE
IF "%choice%"=="2" GOTO RESTORE_LATEST
IF "%choice%"=="3" GOTO RESTORE_SELECT

echo Invalid option. Exiting...
goto END

:SAVE
IF NOT EXIST ".git" (
    echo Initializing Git repository...
    git init
)

echo Staging all changes...
git add .

REM Get current date and time for commit message
FOR /F "tokens=1-4 delims=/- " %%A IN ("%date%") DO (
    SET MYDATE=%%A-%%B-%%C
)
FOR /F "tokens=1-2 delims=: " %%A IN ("%time%") DO (
    SET MYTIME=%%A-%%B
)

SET COMMIT_MSG=save_snapshot_%MYDATE%_%MYTIME%

echo Committing: %COMMIT_MSG%
git commit -m "%COMMIT_MSG%"
echo ✅ Snapshot saved successfully!
goto END

:RESTORE_LATEST
echo Restoring the latest snapshot...
FOR /F "delims=" %%i IN ('git rev-parse HEAD') DO (
    SET LAST_COMMIT=%%i
)

IF NOT DEFINED LAST_COMMIT (
    echo ❌ No commits found. Please save a snapshot first.
    goto END
)

echo Will restore to: !LAST_COMMIT!
echo ⚠️ All uncommitted changes will be lost.
pause
git reset --hard !LAST_COMMIT!
echo ✅ Restore completed!
goto END

:RESTORE_SELECT
echo Listing all snapshots:
set i=0
for /f "delims=" %%L in ('git log --oneline') do (
    set /a i+=1
    set "line[!i!]=%%L"
)

if "!i!"=="0" (
    echo ❌ No snapshots found. Please create one first.
    goto END
)

echo.
for /l %%j in (1,1,!i!) do (
    echo   %%j. !line[%%j]!
)

echo.
set /p select=Enter snapshot number to restore (1~!i!): 

if "!line[%select%]!"=="" (
    echo ❌ Invalid number.
    goto END
)

REM Extract commit ID
for /f "tokens=1" %%x in ("!line[%select%]!") do (
    set "commit_id=%%x"
)

echo.
echo Will restore to commit: !commit_id!
echo ⚠️ All uncommitted changes will be lost.
pause
git reset --hard !commit_id!
echo ✅ Restore successful!
goto END

:END
echo.
pause
