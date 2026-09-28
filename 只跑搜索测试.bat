@echo off
chcp 65001 >nul
echo ========================================
echo   只运行搜索功能测试
echo ========================================
echo.

cd /d "%~dp0"
"%~dp0venv\Scripts\python.exe" -m pytest tests/test_search.py -v --html=reports/search_report.html --self-contained-html

echo.
echo ========================================
echo  完成！报告: reports\search_report.html
echo ========================================
pause
