@echo off
python D:\manager365\PingE5_App.py


REM Gọi script Python và lưu kết quả vào file tạm
python processcheck.py > temp_output.txt

REM Kiểm tra kết quả
findstr /C:"True" temp_output.txt >nul
if %errorlevel%==0 (
    echo Steam or Client is running. Exiting batch script.
    del temp_output.txt
    exit /b
)

REM Nếu không tìm thấy, tiếp tục các lệnh tiếp theo
echo Neither Steam nor Client is running. Continuing...
rem === Thêm lệnh tiếp theo ở đây ===
rem ví dụ:
echo Launching another app...

del temp_output.txt

timeout /t 120
rem rundll32.exe powrprof.dll,SetSuspendState Sleep