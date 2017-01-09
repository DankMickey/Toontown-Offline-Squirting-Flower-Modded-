@echo off
title TCP Buffer Increase
cls
echo Please wait while we change a compatibility setting...
netsh interface tcp set global autotuninglevel=normal
echo Inporting patch. Please wait...
regedit /S tcpbuffersize.reg
echo Patch successful! You may delete this file after reboot. Have fun in Toontown! :)
pause