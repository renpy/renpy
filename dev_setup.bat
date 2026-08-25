@echo off
rem Sets up this checkout for development, using a nightly build for the
rem compiled parts. See dev_setup.py for the details and options.

where py >nul 2>nul
if %errorlevel% == 0 (
    py -3 "%~dp0dev_setup.py" %*
    exit /b %errorlevel%
)

where python >nul 2>nul
if %errorlevel% == 0 (
    python "%~dp0dev_setup.py" %*
    exit /b %errorlevel%
)

echo dev_setup.bat: Python 3 is needed to run dev_setup.py. Install it from https://www.python.org/ and make sure it is on the PATH.
exit /b 1
