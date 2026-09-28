@echo off
chcp 65001 >nul
echo ========================================
echo   Selenium 自动化测试 - 运行全部测试
echo ========================================
echo.
echo 正在启动测试，请稍候...
echo 测试过程中会自动打开 Chrome 浏览器
echo.

cd /d "%~dp0"
"%~dp0venv\Scripts\python.exe" run_tests.py

echo.
echo ========================================
echo  测试完成！报告在 reports 文件夹中
echo ========================================
pause
