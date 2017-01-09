@echo off
title Toontown Offline Client / server Launcher

cd..

echo ===============================
echo Choose your game server!
echo #1 - Localhost
echo #2 - Mini-Server
echo ===============================
echo.
set /P SetInput=
set TTOFF_GAMESERVER=unset

if %SetInput%==1 set TTOFF_GAMESERVER=127.0.0.1
if %SetInput%==2 (set /P TTOFF_GAMESERVER="Connection Ip: " || ^
set TTOFF_GAMESERVER=%TTOFF_GAMESERVER1%
)	
if %TTOFF_GAMESERVER%==unset (
    echo.
    set /P TTOFF_GAMESERVER=Gameserver:
)

echo.
set /P TTOFF_PLAYCOOKIE=Username: 

set TTOFF_PLAYCOOKIE=%TTOFF_PLAYCOOKIE%

echo ===============================
echo Starting Toontown Offline Beta 1 v2 ...
echo Username: %TTOFF_PLAYCOOKIE%
echo Gameserver: %TTOFF_GAMESERVER%
echo ===============================

if %SetInput%==2 (
C:\Panda3D-1.8.1\python\ppython -m GameStart.pyc
pause
) 
   else 
   (
     C:\Panda3D-1.8.1\python\ppython -m GameStart.pyc
	 
    )

pause