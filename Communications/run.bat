@echo off
REM Check if Python is installed
where.exe python >nul 2>nul
if %errorlevel% equ 0 (
    echo starting pip installation if you don't want to play the game please close this command prompt
    timeout /t 10  

    REM Install Flask
    pip install flask    
    REM Install Flask-HTTPAuth
    pip install flask_httpauth    
    REM Install gspread
    pip install gspread    
    REM Install oauth2client
    pip install oauth2client           
    if %errorlevel% equ 0 (
        REM Run the Python script
        start python OnlineServer.py

        REM Start ngrok server
        start "" ngrok http 5000   
    )      
    
) else (
    echo Error: Python is not installed.
    echo Please download and install Python from https://www.python.org/downloads/
    pause
    exit
)

