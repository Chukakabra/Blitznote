@echo off

echo The script for preparing Blitznote for use.
echo Blitznote is written in Python and has open source code on Github.
echo 1.0 release by @CITRUS (Chukakabra). https://github.com/Chukakabra/Blitznote
pause

echo Gathering current user...
set "TARGET_DIR=C:\Users\%USERNAME%\blitznotes"
set "EXECUTABLE_FILE=blitznotes.exe"
set "AHK_SCRIPT=blitznote_ahk.exe"
set "STARTUP_DIR=C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

echo Checking if app's base-directory does exist...
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"
echo Checking if executable file is there...
if not exist "%TARGET_DIR%\%EXECUTABLE_FILE%" (
	echo Oops, it's not! Checking if it's right here...
	if exist "%~dp0%EXECUTABLE_FILE%" (
		echo Got it! Moving it to the app's base-directory...
		move /y "%~dp0%EXECUTABLE_FILE%" "%TARGET_DIR%"
		echo Success.
	) else (
		echo 	Error: Executable file not found. Please, place it in the same directory as blitznote_bind.bat file, or manually move it to C:\Users\[Current user]\blitznotes\.
		pause
		exit /b 1
	)
)

echo Checking if blitznote_ahk is in the blitznote_bin.bat file's directory...
if not exist "%~dp0%AHK_SCRIPT%" (
	echo 	Error: Oops, it's not! Please, place it in the same directory as .bat file.
	pause
	exit /b 1
)


echo Binding app's startup...
move /y "%~dp0%AHK_SCRIPT%" "%STARTUP_DIR%\"
start "" "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\blitznote_ahk.exe"
echo The script made it's work! Try running Blitznote by pressing Ctrl+Shift+B.
pause
exit /b 1