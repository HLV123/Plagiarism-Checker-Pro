@echo off
REM run.bat - Script để chạy Plagiarism Checker trên Windows

echo ================================
echo   PLAGIARISM CHECKER LAUNCHER
echo ================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python không được cài đặt hoặc không có trong PATH
    echo Vui lòng cài đặt Python từ https://python.org
    pause
    exit /b 1
)

echo [INFO] Đã tìm thấy Python
echo.

REM Kiểm tra và cài đặt requirements
echo [INFO] Đang kiểm tra thư viện cần thiết...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo [WARNING] Có lỗi khi cài đặt thư viện
    echo Thử cài đặt thủ công: pip install requests
    echo.
)

REM Chạy ứng dụng
echo [INFO] Đang khởi động Plagiarism Checker...
echo.
python main.py

REM Tạm dừng nếu có lỗi
if errorlevel 1 (
    echo.
    echo [ERROR] Ứng dụng gặp lỗi khi chạy
    pause
)

echo.
echo [INFO] Cảm ơn bạn đã sử dụng Plagiarism Checker!
pause