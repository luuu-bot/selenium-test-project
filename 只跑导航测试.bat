@echo off
chcp 65001 >nul
echo ========================================
echo   只运行导航功能测试
echo ========================================
echo.

cd /d "%~dp0"
"%~dp0venv\Scripts\python.exe" -m pytest tests/test_navigation.py -v --html=reports/navigation_report.html --self-contained-html

echo.
echo ========================================
echo  完成！报告: reports\navigation_report.html
echo ========================================
pause
