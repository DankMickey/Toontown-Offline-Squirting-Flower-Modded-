@echo off

set ttiUsername=username
set ttiPassword=password
set TTI_PLAYCOOKIE=%ttiUsername%
set TTI_GAMESERVER=127.0.0.1

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo _______________________________
echo Toontown is starting. Please be
echo paitent, as the length of this
echo process is based on your
echo computer's speed.
echo ________________________________

%PPYTHON_PATH% -m toontown.toonbase.ToontownStart
pause
