@echo off

SET BASE_PATH=%~dp0
SET PLUGIN_DIR_PATH=%BASE_PATH:~0,-1%
for %%I in ("%PLUGIN_DIR_PATH%") do set PLUGIN_NAME=%%~nxI
SET PLUGIN_LOGS_DIR_PATH=%PLUGIN_DIR_PATH%\logs
SET PYTHON_INIT_PATH=%PLUGIN_DIR_PATH%\init.py

SET PYTHON_COMMAND=%PLUGIN_DIR_PATH%\python312-embedded\python.exe
SET PYTHON_OK_VERSION=Python 3
SET PYTHON_MINIMUM_VERSION=3.8

SET PLUGIN_CODE_DIR_PATH=%PLUGIN_DIR_PATH%\code
SET PLUGIN_CODE_REQUIREMENTS_PATH=%PLUGIN_CODE_DIR_PATH%\requirements.txt
SET PLUGIN_CODE_PATH=%PLUGIN_CODE_DIR_PATH%\main.py

echo "%PYTHON_COMMAND%"
echo "%PYTHON_OK_VERSION%"
echo "%PYTHON_MINIMUM_VERSION%"

echo "%BASE_PATH%"
echo "%PLUGIN_DIR_PATH%"
echo "%PLUGIN_NAME%"
echo "%PLUGIN_LOGS_DIR_PATH%"
echo "%PYTHON_INIT_PATH%"

echo "%PLUGIN_CODE_DIR_PATH%"
echo "%PLUGIN_CODE_REQUIREMENTS_PATH%"
echo "%PLUGIN_CODE_PATH%"

FOR /F "tokens=* USEBACKQ" %%F IN (`%PYTHON_COMMAND% -V`) DO SET PYTHON_VERSION=%%F
echo "%PYTHON_VERSION%"

IF "%PYTHON_VERSION%" == "" (
    echo "bad python"
    powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('%PYTHON_OK_VERSION% not installed', 'Stream Deck plugin \"%PLUGIN_NAME%\" ERROR', 'OK', [System.Windows.Forms.MessageBoxIcon]::Information);}"
    exit
)

IF NOT "%PYTHON_VERSION:~0,8%" == "%PYTHON_OK_VERSION%" (
    echo "bad python"
    powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('%PYTHON_OK_VERSION% not installed', 'Stream Deck plugin \"%PLUGIN_NAME%\" ERROR', 'OK', [System.Windows.Forms.MessageBoxIcon]::Information);}"
    exit
)

SET PYTHONPATH="%PLUGIN_CODE_DIR_PATH%"
echo "%PYTHONPATH%"

"%PYTHON_COMMAND%" "%PLUGIN_CODE_PATH%" %*
