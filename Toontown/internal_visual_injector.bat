@echo off

set TT_PLAYCOOKIE=username
set TT_GAMESERVER=127.0.0.1

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo _______________________________
echo Toontown is starting with a Python
echo injector. Please DO NOT report any
echo bugs you find while using injector
echo codes. They will be ignored.
echo ________________________________

%PPYTHON_PATH% -m toontown.toonbase.ToontownStartWithInjector
pause
