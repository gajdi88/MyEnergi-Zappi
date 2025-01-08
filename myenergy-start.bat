REM Activate the virtual environment
call venv\Scripts\activate

REM Start the Flask app in a detached process
start /b python app.py

REM Open the default web browser to 127.0.0.1:5000
start http://127.0.0.1:5000

REM Deactivate the virtual environment
deactivate

REM Close the batch script console
exit